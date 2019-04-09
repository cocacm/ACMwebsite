# ACMwebsite
Website work in progress for Canyons ACM

* created the flaskr/ directory
* created  `__init__.py` within flaskr/
* defined  `create_app` function ('application factory')
* tell flask where to find the application and run in dev mode:
  > `$ export FLASK_APP=flaskr`
  > `$ export FLASK_ENV=development`
  > `$ flask run`
NOTE: SQLite is convenient because it doesn’t require setting up a separate database server and is built-in to Python. However, if concurrent requests try to write to the database at the same time, they will slow down as each write happens sequentially. Small applications won’t notice this. Once you become big, you may want to switch to a different database.

* view the site by visiting `http://127.0.0.1:5000/hello`
* created a connection to the SQLite database
* created the `init-db` CLI tool in `db.py`
* created a blueprint for authentication
* import and register the blueprint from `__init__.py`
* defined the `/register` view using the auth blueprint
* defined the `/login` view using the auth blueprint
* defined and registered the functions for load_logged_in_user and logout
* created `base.html` as the default html boiler code for each view
* created `auth/register.html` and `auth/login.html` which extend `base.html`
