import traceback
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from app.repositories.server_log_repository import ServerLogRepository
from app.models.mongo.server_log import ServerLog, datetime, HttpRequest
import app.router as app_router
from os import getenv


async def setBody(request: Request):
    if 'content-type' not in request.headers:
        return

    if request.headers['content-type'] == 'application/json':
        body = await request.json()
        request.state.body = body

asgi_app = FastAPI(dependencies=[Depends(setBody)])
asgi_app.include_router(app_router.SearchRouter)
asgi_app.include_router(app_router.ProductRouter)
asgi_app.include_router(app_router.SubscriberRouter)
asgi_app.include_router(app_router.IntergrationRouter)


@asgi_app.on_event('startup')
def check_env():
    mongo_conn_str = getenv('mongo_conn_str')
    if mongo_conn_str is None:
        raise KeyError('env: mongo_conn_str not setup..')

    gcp_intergration_topic_path = getenv('gcp_intergration_topic_path')
    if gcp_intergration_topic_path is None:
        raise KeyError('evn: append_line_notify_endpoint not setup...')

    GOOGLE_APPLICATION_CREDENTIALS = getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if GOOGLE_APPLICATION_CREDENTIALS is None:
        raise KeyError('env: GOOGLE_APPLICATION_CREDENTIALS not setup...')


@asgi_app.middleware('http')
async def error_handler(request: Request, call_next):

    conn_str = getenv("mongo_conn_str")
    with MongoClient(conn_str) as client:
        repo = ServerLogRepository(client)

        start_time = datetime.now()
        try:
            response: Response = await call_next(request)
            process_time = int(
                (datetime.now() - start_time).microseconds / 1000)
            body = request.state.body if hasattr(
                request.state, 'body') else None
            req = HttpRequest(
                path=str(request.url),
                method=request.method,
                body=body
            )
            repo.insert_log(ServerLog(
                start_time=start_time,
                process_time=process_time,
                request=req,
                response_status=response.status_code,
                error=None
            ))
            return response

        except Exception:
            process_time = int(
                (datetime.now() - start_time).microseconds / 1000)
            body = request.state.body if hasattr(
                request.state, 'body') else None
            req = HttpRequest(
                path=str(request.url),
                method=request.method,
                body=body
            )
            error = traceback.format_exc()
            repo.insert_log(ServerLog(
                start_time=start_time,
                process_time=process_time,
                request=req,
                response_status=500,
                error=error
            ))
            raise


@asgi_app.get('/')
def index():
    return RedirectResponse('/docs')
