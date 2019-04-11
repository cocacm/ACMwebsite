"""
this file will contain the `application factory`
also signals to python that flaskr/ is a package
"""
import os
from flask import Flask
from flask import render_template

def create_app(test_config=None):
    # create and configure the application, directory will be relative to this file
    app = Flask(__name__, instance_relative_config=True)

    # an instance folder containing the following should be located outside flaskr/
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
        # uses os library to convert relative db dir to usable path
    )

    if test_config is None:
        # load the instance folder config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test_config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists (flask does not auto-create these)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page to demonstrate routing
    @app.route('/hello')
    # associated the hello() function with the /hello url postfix
    def hello():
        return 'Canyons ACM says: Hello, World!'

    # import the db and run init_app
    from . import db
    db.init_app(app)

    # import and register the auth blueprint
    from . import auth
    from . import blog
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app
