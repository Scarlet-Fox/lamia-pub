"""Lamia is an ActivityPub federating social network site server that
supports blogs, status updates, and polls.
"""
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import lamia.config as CONFIG
from lamia.translation import _
from lamia.database import setup_db
from lamia.email import setup_email
from lamia.logging import logging

app = Starlette(debug=CONFIG.DEBUG)  # pylint: disable=invalid-name
setup_db(app)
setup_email(app)
# TODO: Setup redis here

# Static content loading
app.mount('/static', StaticFiles(directory='statics'), name='static')

# There's probably a more graceful way to do this (a la blueprints)
# Note: the pylint disable address the fact that these imports are not in the
# pythonic place for them (normally, at the top of a file).
# pylint: disable=C0413
import lamia.views
