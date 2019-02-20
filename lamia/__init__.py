"""Lamia is an ActivityPub federating social network site server that
supports blogs, status updates, and polls.
"""
from starlette.applications import Starlette
# from lamia.database import setup_db
from lamia.email import setup_email
from lamia.routes import setup_routes
from lamia.logging import logging
import lamia.config as CONFIG

app = Starlette(debug=CONFIG.DEBUG)  # pylint: disable=invalid-name
setup_email(app)
# TODO: Setup redis here
setup_routes(app)
