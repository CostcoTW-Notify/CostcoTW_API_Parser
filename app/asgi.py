
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

asgi_app = FastAPI()


@asgi_app.get('/')
def index():
    return RedirectResponse('/docs')
