"""
a blueprint for the user authentication services, sets up
routing for the /register and /login url postfix
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# associates the URL `/register` with the register view function below
@bp.route('/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # start validating the input
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        email = request.form['email']
        phonenum = request.form['phonenum']

        db = get_db()
        error = None

        # validate the `username` and `password` are not empty
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        # takes a SQL query with ? placeholders for user input
        # database library will escape values to prevent SQL injection attack
        # if fetchone() finds an existing username entry, user is already registered
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',(username,)
        ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, email, phonenum, fullname) VALUES (?, ?, ?, ?,?)',
                (username, generate_password_hash(password), email, phonenum, fullname)
            )
            # this query modified data => use commit()
            db.commit()

            # after storing the user, redirect them to login page
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

# associates the URL `/login` with the login view function below
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # query the database for the given username
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

# registers a function that will run before the view function, no matter the url
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        print(user_id)
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (str(user_id))
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
