"""This is a quick-and-dirty module for tying Gino to Starlette so that the
database connections can be cleaned up at the end of a Starlette lifecycle.

This module also implements a get_or_404 method that is Starlette compatible
for all of the primary gino classes. If any of these classes will be
instantiated for a Starlette project, then use the variants in this file
in order to have a working get_or_404 method.

Note: The *_or_404 methods here can return quite a few class types because
the returned class will depend on the model that we're looking for. As a
result, they are typed to Any.
"""
import asyncio
import sys

from typing import Any
from sqlalchemy.engine.url import URL
from gino.api import Gino as _Gino, GinoExecutor as _Executor
from gino.engine import GinoConnection as _Connection, GinoEngine as _Engine
from gino.strategies import GinoStrategy
from asyncpg.exceptions import InvalidAuthorizationSpecificationError
from starlette.datastructures import URL, Secret
from starlette.exceptions import HTTPException
from starlette.config import Config

# pylint: disable=too-few-public-methods
# Escaping because these are all subclasses


class StarletteModelMixin:
    """This model mixin will be applied to gino models, giving us an easy way
    to call get_or_404.
    """

    @classmethod
    async def get_or_404(cls: Any, *args, **kwargs) -> Any:
        """Adds a get_or_404 method using Starlette's 404 exception class."""
        initial_query = await cls.get(*args, **kwargs)
        if initial_query is None:
            raise HTTPException(404)
        return initial_query


class GinoExecutor(_Executor):
    """The GinoExecutor is the default extension for implicit execution
    (query chaining from a Gino model). Great place for a first_or_404.
    """

    async def first_or_404(self, *args, **kwargs) -> Any:
        """Adds a get_or_404 method using Starlette's 404 exception class."""
        initial_query = await self.first(*args, **kwargs)
        if initial_query is None:
            raise HTTPException(404)
        return initial_query


class GinoConnection(_Connection):
    """Just a gino connection. We probably want ours to have some slice of
    life stuff here.
    """

    async def first_or_404(self, *args, **kwargs) -> Any:
        """Adds a get_or_404 method using Starlette's 404 exception class."""
        initial_query = await self.first(*args, **kwargs)
        if initial_query is None:
            raise HTTPException(404)
        return initial_query


class GinoEngine(_Engine):
    """The database engine used by gino, we're making our own Starlette
    compatible changes here. Again.
    """
    connection_cls = GinoConnection

    async def first_or_404(self, *args, **kwargs) -> Any:
        """Adds a get_or_404 method using Starlette's 404 exception class."""
        initial_query = await self.first(*args, **kwargs)
        if initial_query is None:
            raise HTTPException(404)
        return initial_query


class StarletteStrategy(GinoStrategy):
    """An adaptor that processes arguments and creates a new sqlalchemy
    engine.

    Note: for more information, the following sqlalchemy class can be examined:
        sqlalchemy.engine.strategies.EngineStrategy
    """
    name = 'starlette'
    engine_cls = GinoEngine


# Yes, so, it is actually important to execute the strategy
StarletteStrategy()


class Gino(_Gino):
    """Support Starlette web server.
    The common usage looks like this::
        from starlette.applications import Starlette
        from starlette.config import Config
        import lamia.utilities.gino as gino
        db = gino()
        config = Config('.env')
        app = Starlette()
        db.init_app(app, config)
    By :meth:`init_app` GINO subscribes to a few events on scarlette, so that
    GINO could use database configuration provided in .env file or by environment
    variables to initialize the bound engine. The config includes:
    * ``driver`` - the database driver, default is ``asyncpg``.
    * ``host`` - database server host, default is ``localhost``.
    * ``port`` - database server port, default is ``5432``.
    * ``user`` - database server user, default is ``postgres``.
    * ``password`` - database server password, default is empty.
    * ``database`` - database name, default is ``postgres``.
    * ``dsn`` - a SQLAlchemy database URL to create the engine, its existence
      will replace all previous connect arguments.
    * ``pool_min_size`` - the initial number of connections of the db pool.
    * ``pool_max_size`` - the maximum number of connections in the db pool.
    * ``echo`` - enable SQLAlchemy echo mode.
    * ``ssl`` - SSL context passed to ``asyncpg.connect``, default is ``None``.
    """

    model_base_classes = _Gino.model_base_classes + (StarletteModelMixin, )
    query_executor = GinoExecutor

    def __init__(self, config: Config = None, *args, **kwargs) -> None:  # pylint: disable=keyword-arg-before-vararg
        """Optionally: tie to an app on instantiation."""
        super().__init__(*args, **kwargs)
        self.config = config

    async def startup(self) -> None:
        """Bind a pile of async threads to the database when Starlette starts."""
        if self.config('DB_DSN', default=False):
            dsn = str(self.config('DB_DSN', cast=URL))
        else:
            dsn = URL(
                drivername=self.config(
                    'DB_DRIVER', cast=str, default='asyncpg'),
                host=self.config('DB_HOST', cast=str, default='localhost'),
                port=self.config('DB_PORT', cast=int, default=5432),
                username=self.config('DB_USER', cast=str, default='postgres'),
                password=self.config('DB_PASSWORD', cast=Secret, default=''),
                database=self.config(
                    'DB_DATABASE', cast=str, default='postgres'),
            )

        try:
            await self.set_bind(
                dsn,
                echo=self.config('DB_ECHO', cast=bool, default=False),
                logging_name='Cheese',
                min_size=self.config('DB_POOL_MIN_SIZE', cast=int, default=5),
                max_size=self.config('DB_POOL_MAX_SIZE', cast=int, default=10),
                ssl=self.config('DB_SSL', cast=bool, default=None),
                loop=asyncio.get_event_loop(),
            )
        except InvalidAuthorizationSpecificationError:
            sys.exit("""
                InvalidAuthorizationSpecificationError:

                Your database username or password is invalid. Please
                check your config and try again.

                If you did not configure a database, then add a database
                configuration line to your lamia.config file.
                """)
        except ConnectionRefusedError:
            sys.exit("""
                ConnectionRefusedError:

                Check that your database details are in the lamia.config
                file and can actually connect to the database.

                If the database username and password look right, then check
                that your postgreSQL database is online and accepting
                connections at the right port and address.
                """)

    async def shutdown(self) -> None:
        """When Starlette is shutdown, go ahead and close all database
        connections and wait for the close."""
        await self.pop_bind().close()
