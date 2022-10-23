
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse, Response
from fastapi.encoders import jsonable_encoder
import app.router as app_router
from os import getenv

asgi_app = FastAPI()
asgi_app.include_router(app_router.SnapshotRouter)
asgi_app.include_router(app_router.SearchRouter)


@asgi_app.on_event('startup')
def check_env():
    mongo_conn_str = getenv('mongo_conn_str')
    if mongo_conn_str is None:
        raise KeyError('env: mongo_conn_str not setup..')

    name = getenv('snapshot_collection')
    if name is None:
        raise KeyError('env: snapshot_collection_name not setup...')


@asgi_app.middleware('http')
async def error_handler(request: Request, call_next):

    try:
        return await call_next(request)
    except Exception as e:

        error_data = {
            'status': '500',
            'message': 'There are some exception occur when process request',
            'request_url': request.url,
            'error': str(e)
        }
        json = jsonable_encoder(error_data)
        return JSONResponse(
            status_code=200,
            content=json)


@asgi_app.get('/')
def index():
    return RedirectResponse('/docs')
