import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email, date, time):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    subject = "Session Booking Confirmed"
    body = f"Your session is booked on {date} at {time}"

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

        print("Email sent to", to_email)

    except Exception as e:
        print("Email failed:", e)
