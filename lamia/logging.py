"""Included this code to change gino's logging level. This prevents some double
logging that was making my lose my mind with uvicorn's defaults.
"""
import logging
import lamia.config as CONFIG
from lamia.translation import _

logging.basicConfig()
logging.getLogger('gino').setLevel(logging.WARN)

# Debug messages only when in debug mode
if CONFIG.DEBUG:
    logging.getLogger().setLevel(CONFIG.DEBUG)

    # This should be translated to true to show that translation is not failing
    logging.debug(_("Translation is working: False"))
