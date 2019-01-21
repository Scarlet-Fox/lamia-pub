from starlette.applications import Starlette
from starlette.config import Config
from .middleware.gino import Gino

# Included this code to change gino's logging level. This prevents some double
# logging that was making my lose my mind with uvicorn's defaults.
import logging
logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)
# Initialize the app, including the database connection.
db = Gino()
config = Config('.env')
app = Starlette(debug=config("DEBUG", cast=bool, default=False))
db.init_app(app, config)
# TODO: Setup redis here

# There's probably a more graceful way to do this (a la blueprints)
from .views import core
