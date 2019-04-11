import flask
import flaskr.auth 
import flaskr.db
from werkzeug.exceptions import abort

bp = flask.Blueprint('blog', __name__)

def get_post(id, check_author=True):
    post = flaskr.db.get_db().execute(
        'SELECT p.id, title, content, created, author_id, p.username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post == None:
        abort(404, "Does not exist")
    if check_author and post['author_id'] != flask.g.user['id']:
        abort(403)
    return post

@bp.route('/')
def index():
    database = flaskr.db.get_db()
    posts = database.execute('SELECT p.id, title, content, created, author_id, p.username FROM POST p JOIN USER u ON p.author_id = u.id ORDER BY created DESC;').fetchall()
    #posts = database.execute('SELECT * FROM POST ORDER BY created').fetchall()
    return flask.render_template('blog/index.html', posts=posts)
@flaskr.auth.login_required
@bp.route('/create', methods=('GET', 'POST'))
def create_post():
    if flask.request.method=='POST' and flask.g.user['isOfficer'] == True:
        title = flask.request.form['title']
        content = flask.request.form['content']
        error = None
        if not title:
            error = 'Title required'
        if not content:
            error = 'The body is blank'
        if error is not None:
            flask.flash(error)
        else:
            database = flaskr.db.get_db()
            database.execute('INSERT INTO POST (title, content, author_id, username)'
                            'VALUES (?, ?, ?,?)', (title, content, flask.g.user['id'], flask.g.user['username']))
            database.commit()
            return flask.redirect(flask.url_for('blog.index'))
    else:
        abort(403)
    return flask.render_template('blog/create.html')
@flaskr.auth.login_required
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update_post(id):
    post = get_post(id)
       
    if flask.request.method == 'POST':
        title = flask.request.form['title']
        content = flask.request.form['content']
        error = None

        if not title:
            error = 'Title is required'
        if not content:
            error = 'No content'
        if error is not None:
            flask.flash(error)
        else: 
            db = flaskr.db.get_db()
            db.execute(
                'UPDATE post SET title = ?, content = ? WHERE id = ?',
                (title, content, id)
            )
            db.commit()
            return flask.redirect(flask.url_for('blog.index'))
    return flask.render_template('blog/update.html', post=post)

@flaskr.auth.login_required
@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = flaskr.db.get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return flask.redirect(flask.url_for('blog.index'))
        
