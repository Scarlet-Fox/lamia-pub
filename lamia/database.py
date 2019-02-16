"""Setup lamia database access for gino models here."""
# pylint: disable=invalid-name
import lamia.utilities.gino as gino
import lamia.config as CONFIG

db = gino.Gino()

def setup_db(app) -> None:
    db.init_app(app, CONFIG.config)
    