from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from .. import app
from .. import db
from .. import jinja
from .. import config


@app.route('/')
async def introduction(request):
    template = jinja.get_template('index.html')
    content = template.render(
        request=request, instance_name=f'{app.instance_name}')
    return HTMLResponse(content)


# How to get a connection
#async with db.acquire(lazy=True) as connection:
