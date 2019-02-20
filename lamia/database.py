"""Setup lamia database access for gino and gino's lifecycle stuff."""
# pylint: disable=invalid-name
import asyncio
import atexit
from starlette.applications import Starlette
import lamia.utilities.gino as gino
import lamia.config as CONFIG

db = gino.Gino(CONFIG.config)
asyncio.get_event_loop().run_until_complete(db.startup())

def shutdown_db() -> None:
    asyncio.run_coroutine_threadsafe(db.shutdown(), asyncio.get_event_loop())

atexit.register(shutdown_db)