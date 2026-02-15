import sqlite3
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText


load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    email = request.form["email"]
    date = request.form["date"]
    time = request.form["time"]

    result = add_booking(name, email, date, time)

    if result:
        return render_template("success.html")
    else:
        return render_template("fail.html")

@app.route("/admin")
def admin():
    booking_data = get_all_bookings()
    return render_template("admin.html", bookings=booking_data)


def create_table():
    conn = sqlite3.connect(database="database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Table created successfully.")

def add_booking(name, email, date, time):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # <------- Preventing double booking ------>
    cursor.execute("""
            SELECT * FROM bookings
            WHERE date=? AND time=?
        """, (date, time))

    existing = cursor.fetchone()

    if existing:
        print("Slot already booked")
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO bookings (name, email, date, time)
        VALUES (?, ?, ?, ?)
    """, (name, email, date, time))

    conn.commit()
    conn.close()

    print("Booking added successfully")
    send_email(email, date, time)
    return True

def get_all_bookings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    conn.close()
    return rows

def send_email(to_email, date, time):

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    subject = "Session Booking Confirmed"
    body = f"Your session is booked on {date} at {time}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender_email, sender_password)

    server.send_message(msg)
    server.quit()

    print("Email sent successfully")



if __name__ == "__main__":
    create_table()
    # add_booking("Manglam", "test@mail.com", "15-02-2026", "10:00")
    add_booking("A", "a@mail.com", "20-02-2026", "10:00")
    add_booking("B", "b@mail.com", "20-02-2026", "10:00")

    # PRINT ALL BOOKINGS
    data = get_all_bookings()
    print("All bookings:", data)

    app.run(debug=True)

