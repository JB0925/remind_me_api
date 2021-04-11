import fastapi
from starlette.staticfiles import StaticFiles
import uvicorn

from remind_me_api.views import all_views
from remind_me_api.data.db_session import global_init
from remind_me_api.services.message_service import check_and_run_jobs

api = fastapi.FastAPI()


def configure_routes():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(all_views.router)


def configure_db():
    global_init()


def main():
    configure_routes()
    configure_db()
    uvicorn.run(api, port=8000, host='127.0.0.1')
    check_and_run_jobs()


if __name__ == '__main__':
    main()
else:
    configure_routes()
    configure_db()
    check_and_run_jobs()