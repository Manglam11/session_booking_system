from flask import Flask, render_template, request
from db import create_table, add_booking, get_all_bookings
from email_utils import send_confirmation_email
from scheduler import schedule_reminder
from logger_config import logger


app = Flask(__name__)


@app.route("/")
def home():
    logger.info("Home page opened")
    return render_template("index.html")


@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    email = request.form["email"]
    date = request.form["date"]
    time = request.form["time"]

    success = add_booking(name, email, date, time)

    if success:
        send_confirmation_email(email, date, time)
        schedule_reminder(email, date, time)
        return render_template("success.html")

    return render_template("fail.html")


@app.route("/admin")
def admin():
    logger.info("Admin panel viewed")
    bookings = get_all_bookings()
    return render_template("admin.html", bookings=bookings)


if __name__ == "__main__":
    create_table()
    # add_booking("Manglam", "test@mail.com", "15-02-2026", "10:00")
    app.run(debug=True)





