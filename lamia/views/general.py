#TODO: Remove this pylint statment when this file isn't super WIP
# pylint: skip-file
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from .. import app
from .. import db
from lamia.templating import jinja
from .. import config


@app.route('/')
async def introduction(request):
    template = jinja.get_template('index.html')
    content = template.render(request=request, site_name=f'{app.site_name}')
    return HTMLResponse(content)


# How to get a connection
#async with db.acquire(lazy=True) as connection:
