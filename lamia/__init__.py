"""Lamia is an ActivityPub federating social network site server that
supports blogs, status updates, and polls.
"""
import logging
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import lamia
import lamia.utilities.gino as gino
import lamia.utilities.email as email
import lamia.config as CONFIG
from lamia.translation import _

# TODO : mypy

# Included this code to change gino's logging level. This prevents some double
# logging that was making my lose my mind with uvicorn's defaults.
logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)

# Initialize the app, including the database connection.
# disabling pylint warning, as this is conventional for these packages

db = gino.Gino()
mail = email.Email()
app = Starlette(debug=CONFIG.DEBUG)
db.init_app(app, CONFIG.config)
mail.init_app(app, CONFIG.config)
# pylint: enable=invalid-name
# This should be translated to true to show that translation is not failing

# Debug messages only when in debug mode
if CONFIG.DEBUG:
    logging.getLogger().setLevel(CONFIG.DEBUG)

logging.debug(_("Translation is working: False"))
# Some config loading
app.site_name = CONFIG.SITE_NAME

# pylint: enable=invalid-name
# Static content loading
app.mount('/static', StaticFiles(directory='statics'), name='static')

# TODO: Setup redis here

# There's probably a more graceful way to do this (a la blueprints)
# Note: the pylint disable address the fact that these imports are not in the
# pythonic place for them (normally, at the top of a file).
from .views import general  # pylint: disable=C0413
