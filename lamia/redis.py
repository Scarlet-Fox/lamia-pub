"""Redis binder for starlette."""
from starlette.applications import Starlette
import lamia.utilities.redis as redis
import lamia.config as CONFIG

redis = redis.Redis()  # pylint: disable=invalid-name


def setup_redis(app: Starlette) -> None:
    """Ties redis binding to starlette app."""
    redis.init_app(app, CONFIG.config)
