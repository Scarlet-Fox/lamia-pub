from starlette.responses import JSONResponse
from .. import app
from .. import db

@app.route('/')
async def introduction(request):
    async with db.acquire(lazy=True) as connection:
        return JSONResponse({'time': str(await connection.scalar('select now()'))})
