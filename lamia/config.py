"""This module pulls in the configuration details from a lamia.config or
lamia.dev.config file.
"""
from starlette.config import Config
from lamia.translation import gettext as _

config = Config('lamia.config')  # pylint: disable=invalid-name

DEBUG = config('DEBUG', cast=bool, default=False)
SITE_NAME = config('SITE_NAME', cast=str, default=_('A Lamia Community'))
TEMPLATE_RELOAD = config(
    "TEMPLATE_RELOAD",
    cast=bool,
    default=False,
)
BASE_URL = config('BASE_URL', cast=str)
