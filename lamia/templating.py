"""Setup lamia templating here."""
import os
import jinja2
from lamia.translation import EN
import lamia.config as CONFIG


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


TEMPLATES_DIRS = [
    os.path.dirname(__file__) + '/templates',
]

# pylint: disable=invalid-name
# same rational as above
jinja = setup_jinja2(TEMPLATES_DIRS, CONFIG.TEMPLATE_RELOAD)
