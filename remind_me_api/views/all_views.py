from typing import List, Optional
import json

import fastapi
from sqlalchemy.sql.functions import user
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import requests

from remind_me_api.services.message_service import check_and_run_jobs
from remind_me_api.data.events import Events
from remind_me_api.data import db_session
from remind_me_api.services.store_and_query_jobs import save_messages, query_number, jsonify_jobs

templates = Jinja2Templates('templates')
router = fastapi.APIRouter()


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/api/jobs/{number}')
def display_jobs(request: Request, number: str): 
    jobs = query_number(number)
    if jobs:
        user_jobs = jsonify_jobs(jobs)
        return user_jobs
    else:
        return {'jobs_by_this_number': 'None'}