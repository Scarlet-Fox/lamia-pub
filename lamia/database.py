"""Setup lamia database access for gino and gino's lifecycle stuff."""
# pylint: disable=invalid-name
import asyncio
import atexit
import lamia.utilities.gino as gino
import lamia.config as CONFIG

db = gino.Gino(CONFIG.config)
loop = asyncio.get_event_loop()
loop.run_until_complete(db.startup())


def shutdown_db() -> None:
    """Syncronous function that runs the gino shutdown method in a threadsafe
    bubble so that the shutdown can occur when the lamia server exits.
    """
    asyncio.run_coroutine_threadsafe(db.shutdown(), asyncio.get_event_loop())


atexit.register(shutdown_db)
