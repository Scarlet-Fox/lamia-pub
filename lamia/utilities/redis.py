"""Lamia wrapper for aioredis.

Creates a unified interface with the set redis server.

Adds the following configuration settings:

REDIS_DSN: -> url
    URL for redis with shape `redis://[usrname:pass]@hostname`
    username is unused, but if password is included it will be
    used to authenticate with the redis server.

REDIS_NO_PASS: -> bool
    Supresses warning of no password on redis server, as a
    positive confirmation that the server has been secured.

REDIS_MIN_POOL: -> int
    Sets the minimum number of pool workers, default is 1.

REDIS_MAX_POOL: -> int
    Sets the maximum number of pool workers, defualt is 10.

"""
import sys

import aioredis
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import URL

from lamia.logging import logging
from lamia.translation import _


class Redis():
    """Redis binding for starlette

    app: optional starlette app
    config: optional starlette config object

    one or both arguments are not included, init_app will need to be
    called with both in order for binding to the starlette lifetime
    to occur. If both are provided than init_app will be called internally.
    """

    def init_app(self, app: Starlette, config: Config) -> None:
        """Bind to starlette lifetime.

        app: A Starlette application
        config: A Starlette Config object

        Returns: Nothing
        """
        self.config = config
        app.add_event_handler('startup', self._startup)
        app.add_event_handler('shutdown', self._shutdown)

    def __init__(self, app: Starlette = None, config: Config = None):
        if (app is not None) and (config is not None):
            self.init_app(app, config)

    async def _startup(self) -> None:

        # pylint: disable=attribute-defined-outside-init
        # Disabled because _startup functions as the init method for this class
        self._pool = await aioredis.create_pool(
            str(self.config('REDIS_DSN', cast=URL)),
            minsize=self.config('REDIS_MINPOOL', cast=int, default=1),
            maxsize=self.config('REDIS_MAXPOOL', cast=int, default=10))
        if self.config('REDIS_DSN', cast=URL).password is None\
                and not self.config('REDIS_NO_PASS', cast=bool, default=False):
            logging.warning(
                "REDIS: Was able to connect to redis server without a "
                "password, this could leave your redis server "
                "vulerable, if other security measures are not taken.\n"
                "   Please make sure you have properly "
                "secured the redis server.\n"
                "   This message can be suppresed by setting "
                "REDIS_NO_PASS to True in your configuration file.\n"
                "   Read here for more information on redis security: "
                "https://redis.io/topics/security")
        self.command = aioredis.Redis(self._pool)
        # pylint: enable=attribute-defined-outside-init

    async def _shutdown(self) -> None:
        logging.info(_("REDIS: Shutting down redis pool"))
        self._pool.close()
        await self._pool.wait_closed()
