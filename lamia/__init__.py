from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.config import Config
from .middleware.gino import Gino
import jinja2
import inspect

# TODO : mypy

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


def setup_jinja2(template_dirs):
    """Setup a jinja2 env (https://www.starlette.io/templates/)"""
    @jinja2.contextfunction
    def url_for(context, name, **path_params):
        request = context['request']
        return request.url_for(name, **path_params)

    loader = jinja2.FileSystemLoader(template_dirs)
    env = jinja2.Environment(loader=loader, autoescape=True)
    env.globals['url_for'] = url_for
    return env

templates_dirs = ['templates']
try:
    # I feel like this may not be cool, but it uh works.
    import lamia
    # Damn, I love neat tricks, this looks up the lamia module path.
    module_template_dir = inspect.getfile(lamia)
    # The path includes __init__.py so you have to drop it.
    templates_dirs.append(
        '/'.join(module_template_dir.split("/")[:-1]+['templates'])
    )
except NameError:
    # All is well, just use the ./templates folder
    pass

jinja = setup_jinja2(templates_dirs)
    

# Static content loading
app.mount('/static', StaticFiles(directory='statics'), name='static')

# TODO: Setup redis here


# There's probably a more graceful way to do this (a la blueprints)
from .views import general

