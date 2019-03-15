import asyncio

import aioredis
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import URL

from lamia.logging import logging
from lamia.translation import _

class Redis():

    def init_app(self, app: Starlette, config: Config) -> None:
        self.config = config
        app.add_event_handler('startup', self._startup)
        app.add_event_handler('shutdown', self._shutdown)

    def __init__(self, app: Starlette = None, config: Config = None):
        if (app is not None) and (config is None):
            raise ValueError("A starlette app was provided, but no configuration.")
        if app is not None:
            self.init_app(app, config)
        elif config is not None:
            self.config = config

    async def _startup(self) -> None:

        # pylint: disable=attribute-defined-outside-init
        # Disabled because _startup functions as the init method for this class
        self.redis_pool = await aioredis.create_pool(
            str(self.config('REDIS_DSN', cast=URL)),
            minsize=self.config('REDIS_MINPOOL', cast=int, default=1),
            maxsize=self.config('REDIS_MAXPOOL', cast=int, default=10))
        # pylint: enable=attribute-defined-outside-init

    async def _shutdown(self) -> None:
        logging.info(_("REDIS: Shutting down redis pool"))
        self.redis_pool.close()
        await self.redis_pool.wait_closed()
