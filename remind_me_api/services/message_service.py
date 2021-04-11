import time

from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler

from remind_me_api import check_email
from remind_me_api.sms import PASSWORD, send
from remind_me_api import schedule_jobs
from remind_me_api.services.store_and_query_jobs import save_messages

EMAIL: str = config('EMAIL')
PASSWORD: str = config('PASSWORD')

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def check_email_and_make_jobs() -> None:
    messages = check_email.main()
    if messages:
        save_messages(messages)
        schedule_jobs.main(messages)
        return messages


def check_and_run_jobs():
    scheduler.start()
    print(scheduler.get_jobs())


if __name__ == '__main__':
    check_and_run_jobs()
    