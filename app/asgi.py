
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import app.router as app_router
from os import getenv

asgi_app = FastAPI()
asgi_app.include_router(app_router.SearchRouter)
asgi_app.include_router(app_router.ProductRouter)
asgi_app.include_router(app_router.SubscriberRouter)


@asgi_app.on_event('startup')
def check_env():
    mongo_conn_str = getenv('mongo_conn_str')
    if mongo_conn_str is None:
        raise KeyError('env: mongo_conn_str not setup..')

    append_line_notify_endpoint = getenv('append_line_notify_endpoint')
    if append_line_notify_endpoint is None:
        raise KeyError('evn: append_line_notify_endpoint not setup...')


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
        print("=========== Error ============")
        print(json)
        print("==============================")
        return JSONResponse(
            status_code=400,
            content=json)


@asgi_app.get('/')
def index():
    return RedirectResponse('/docs')
