# License header will go here when I pick one.

from flask import Flask
from flask import session
from flask_session import Session
from flask_assets import Environment, Bundle
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.contrib.cache import RedisCache
from os import path
import configparser
import os

# Try importing psyco cffi for PyPy
try:
    from psycopg2cffi import compat
    compat.register()
except ImportError:
    pass

# Instantiate the app and wire up dependencies
app = Flask(__name__)
bcrypt = Bcrypt(app)
assets = Environment(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.wsgi_app = ProxyFix(app.wsgi_app)

# Debug settings for flask and flask-assets based on env variable
app.config['DEBUG'] = bool(os.environ.get('DEBUG', 1))
app.config['ASSETS_DEBUG'] = app.config['DEBUG']
app.config['TEMPLATES_AUTO_RELOAD'] = app.config['DEBUG']

# This is for signals. Probably won't need it.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

