import json
from typing import List, Optional
from remind_me_api.data import db_session
from remind_me_api.data.events import Events


def save_messages(messages: List) -> None:
    session = db_session.create_session()

    for msg in messages:
        event = Events()
        event.phone_number = msg[0]
        event.carrier = msg[1]
        event.event = msg[2]
        event.date_and_time = msg[3]
        session.add(event)
        session.commit()


def query_number(number: str) -> Optional[List]:
    session = db_session.create_session()
    query = session.query(Events).filter(Events.phone_number == number)
    return [item for item in query] or None


def jsonify_jobs(jobs: List[Events]) -> List[dict]:
    display_list = []
    for job in jobs:
        temp = {
            'id': job.id,
            'date': job.date_and_time,
            'carrier': job.carrier,
            'event': job.event
        }
        display_list.append(temp)
    return display_list