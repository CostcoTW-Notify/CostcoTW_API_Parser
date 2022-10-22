
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from os import getenv

asgi_app = FastAPI()


@asgi_app.on_event('startup')
def check_env():
    mongo_conn_str = getenv('mongo_conn_str')
    if mongo_conn_str is None:
        raise KeyError('env: mongo_conn_str not setup..')

    name = getenv('snapshot_collection')
    if name is None:
        raise KeyError('env: snapshot_collection_name not setup...')


@asgi_app.get('/')
def index():
    return RedirectResponse('/docs')
