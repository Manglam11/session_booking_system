from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from email_utils import send_reminder_email
from logger_config import logger

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_reminder(email, date, time):
    # convert string to datetime
    session_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    reminder_time = session_datetime - timedelta(minutes=1)

    if reminder_time > datetime.now():
        scheduler.add_job(
            send_reminder_email,
            'date',
            run_date=reminder_time,
            args=[email, date, time]
        )

        logger.info(f"Reminder scheduled for {email} at {reminder_time}")
