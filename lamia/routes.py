"""The routes for lamia are configured here. There is no starlette convention
that dictates this. However, doing things this way is more transparent than
calling the app.route decorator from every module that adds some type of
route.

TODO: This file should look for extensions with routes and add them
programmatically.
"""
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import lamia.views.general as lamia_general

def setup_routes(app: Starlette) -> None:
    """Add all of lamia's default routes.
    
    TODO: A different setup function should be added to do the same for
    routes associated with extensions.
    """
    # Static content loading
    app.mount('/static', StaticFiles(directory='statics'), name='static')
    
    # Just a boring test route
    app.add_route('/', lamia_general.introduction, ['GET'])
