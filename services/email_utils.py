import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from services.logger_config import logger

load_dotenv()


# ---------- CORE MAIL SENDER ----------
def send_mail(to_email, subject, body):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        logger.info(f"Email sent to {to_email} | Subject: {subject}")

    except Exception as e:
        logger.error(f"Email failed: {e}")


# ---------- CONFIRMATION EMAIL ----------
def send_confirmation_email(to_email, date, time):
    subject = "Session Booking Confirmed"

    body = f"""
Hello,

Your session has been successfully booked.

Date: {date}
Time: {time}

Please be available 5 minutes before the scheduled time.

Thank you.
TimeSyncer
"""

    send_mail(to_email, subject, body)


# ---------- REMINDER EMAIL ----------
def send_reminder_email(to_email, date, time):
    subject = "Reminder: Your Session Starts Soon"

    body = f"""
Hello,

This is a reminder for your upcoming session.

Date: {date}
Time: {time}

Please join on time.

Regards.
TimeSyncer
"""

    send_mail(to_email, subject, body)
