from starlette.applications import Starlette
import lamia.utilities.redis as redis
import lamia.config as CONFIG

redis = redis.Redis()

def setup_redis(app: Starlette) -> None:
    redis.init_app(app, CONFIG.config)
