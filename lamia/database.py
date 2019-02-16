"""Setup lamia database access for gino and gino's lifecycle stuff."""
# pylint: disable=invalid-name
from starlette.applications import Starlette
import lamia.utilities.gino as gino
import lamia.config as CONFIG

db = gino.Gino()


def setup_db(app: Starlette) -> None:
    """Sets up lifecycle functions."""
    db.init_app(app, CONFIG.config)
