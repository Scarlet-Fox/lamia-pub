"""Lamia is an ActivityPub federating social network site server that
supports blogs, status updates, and polls.
"""

import logging
import jinja2
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import lamia
import lamia.utilities.gino as gino
import lamia.utilities.email as email
import lamia.config as CONFIG
from lamia.translation import gettext as _
from lamia.translation import en as EN

# TODO : mypy

# Included this code to change gino's logging level. This prevents some double
# logging that was making my lose my mind with uvicorn's defaults.
logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)

# Initialize the app, including the database connection.
# disabling pylint warning, as this is conventional for these packages
# pylint: disable=invalid-name
db = gino.Gino()
mail = email.Email()
app = Starlette(debug=CONFIG.DEBUG)
db.init_app(app, CONFIG.config)
mail.init_app(app, CONFIG.config)
# pylint: enable=invalid-name
# This should be translated to true to show that translation is not failing

# Debug messages only when in debug mode
if CONFIG.DEBUG:
    logging.getLogger().setLevel(CONFIG.DEBUG)

logging.debug(_("Translation is working: False"))
# Some config loading
app.site_name = CONFIG.SITE_NAME


# Jinja2 science starts here
def setup_jinja2(template_dirs, auto_reload):
    """Setup a jinja2 env (https://www.starlette.io/templates/)"""

    @jinja2.contextfunction
    def url_for(context, name, **path_params):
        request = context['request']
        return request.url_for(name, **path_params)

    # first check for template overrides on the same level above the modual.
    # check lamia defaults if nothing is found
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(template_dirs),
        jinja2.PackageLoader('lamia')
    ])
    env = jinja2.Environment(
        loader=loader,
        autoescape=True,
        auto_reload=auto_reload,
        extensions=['jinja2.ext.i18n'],
    )
    env.install_gettext_translations(EN)  # pylint: disable=no-member
    env.globals['url_for'] = url_for
    return env


TEMPLATES_DIRS = ['templates']

# pylint: disable=invalid-name
# same rational as above
jinja = setup_jinja2(
    TEMPLATES_DIRS,
    CONFIG.TEMPLATE_RELOAD
)
# pylint: enable=invalid-name
# Static content loading
app.mount('/static', StaticFiles(directory='statics'), name='static')

# TODO: Setup redis here

# There's probably a more graceful way to do this (a la blueprints)
# Note: the pylint disable address the fact that these imports are not in the
# pythonic place for them (normally, at the top of a file).
from .views import general  # pylint: disable=C0413
