from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse
from .. import app
from .. import db
from .. import jinja
from .. import config


@app.route('/')
async def introduction(request):
    template = jinja.get_template('base.html')
    content = template.render(
        request=request,
        title=f'{config.SITE_NAME}'
    )
    return HTMLResponse(content)
    





# How to get a connection
#async with db.acquire(lazy=True) as connection:
        

