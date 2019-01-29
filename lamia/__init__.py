"""Lamia is an ActivityPub federating social network instance server that
supports blogs, status updates, and polls.
"""

import logging
import inspect
import jinja2
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.config import Config
from .middleware.gino import Gino
from .utilities.email import Email

# TODO : mypy

# Included this code to change gino's logging level. This prevents some double
# logging that was making my lose my mind with uvicorn's defaults.
logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)

# Initialize the app, including the database connection.
# disabling pylint warning, as this is conventional for these packages
# pylint: disable=invalid-name
db = Gino()
mail = Email()
config = Config('lamia.config')
app = Starlette(debug=config('DEBUG', cast=bool, default=False))
db.init_app(app, config)
mail.init_app(app, config)
# pylint: enable=invalid-name

# Some config loading
app.instance_name = config(
    'INSTANCE_NAME', cast=str, default='A Lamia Community')


# Jinja2 science starts here
def setup_jinja2(template_dirs, auto_reload):
    """Setup a jinja2 env (https://www.starlette.io/templates/)"""

    @jinja2.contextfunction
    def url_for(context, name, **path_params):
        request = context['request']
        return request.url_for(name, **path_params)

    loader = jinja2.FileSystemLoader(template_dirs)
    env = jinja2.Environment(
        loader=loader,
        autoescape=True,
        auto_reload=auto_reload,
    )
    env.globals['url_for'] = url_for
    return env


TEMPLATES_DIRS = ['templates']
try:
    # I feel like this may not be cool, but it uh works.
    import lamia  # pylint: disable=W0406
    # Damn, I love neat tricks, this looks up the lamia module path.
    MODULE_TEMPLATE_DIR = inspect.getfile(lamia)
    # The path includes __init__.py so you have to drop it.
    templates_dirs.append(
        '/'.join(MODULE_TEMPLATE_DIR.split("/")[:-1] + ['templates']))
except NameError:
    # All is well, just use the ./templates folder
    pass

# pylint: disable=invalid-name
# same rational as above
jinja = setup_jinja2(
    TEMPLATES_DIRS,
    config(
        "TEMPLATE_RELOAD",
        cast=bool,
        default=False,
    ),
)
# pylint: enable=invalid-name

# Static content loading
app.mount('/static', StaticFiles(directory='statics'), name='static')

# TODO: Setup redis here

# There's probably a more graceful way to do this (a la blueprints)
from .views import general  # pylint: disable=C0413
