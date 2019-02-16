"""Lamia is an ActivityPub federating social network site server that
supports blogs, status updates, and polls.
"""
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import lamia.utilities.email as email
import lamia.config as CONFIG
from lamia.translation import _
from lamia.database import setup_db
from lamia.logging import logging

app = Starlette(debug=CONFIG.DEBUG)
setup_db(app)

mail = email.Email()
mail.init_app(app, CONFIG.config)

# Debug messages only when in debug mode
if CONFIG.DEBUG:
    logging.getLogger().setLevel(CONFIG.DEBUG)

    # This should be translated to true to show that translation is not failing
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
# pylint: disable=C0413
import lamia.views