from starlette.applications import Starlette
from starlette.config import Config
from .middleware.gino import Gino

import logging
logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)

db = Gino()
config = Config('.env')
app = Starlette(debug=config("DEBUG", cast=bool, default=False))
db.init_app(app, config)

# Have to import views in order to use them
from .views import core
