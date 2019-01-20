from starlette.applications import Starlette
from starlette.config import Config
from .middleware.gino import Gino

db = Gino()
config = Config('.env')
app = Starlette(debug=True)
db.init_app(app, config)

# Have to import views in order to use them
from .views import core
