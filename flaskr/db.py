"""
links our website to the SQLite database using g,
a unique object created during each request

current_app is an obj which points to the flask app
handling that request
"""
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        # establishes a connection to the file pointed to by 'DATABASE' config key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells the connection to return rows that behave like python dicts
        g.db.row_factory = sqlite3.Row

    # fetched the database
    return g.db

def close_db(e=None):
    # check if g.db was set, otherwise close db
    db = g.pop('db', None)

    if db is not None:
        db.close()

# after creating the SQL schema =>
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # opens a file relative to the flaskr package
        db.executescript(f.read().decode('utf8'))

# defines a CLI cmd called init_db that called this function
@click.command('init-db')
@with_appcontext
def init_db_command():
    # clears existing data and create new tables
    init_db()
    click.echo('initialized the database')

# a function that takes an application and does instance registration
def init_app(app):
    # tells flask to call 'close_db' after returning the response
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the `flask` command
    app.cli.add_command(init_db_command)
