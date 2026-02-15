import sqlite3

from flask import Flask, render_template, request

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
    return True

def get_all_bookings():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    conn.close()
    return rows


if __name__ == "__main__":
    create_table()
    # add_booking("Manglam", "test@mail.com", "15-02-2026", "10:00")
    add_booking("A", "a@mail.com", "20-02-2026", "10:00")
    add_booking("B", "b@mail.com", "20-02-2026", "10:00")

    # PRINT ALL BOOKINGS
    data = get_all_bookings()
    print("All bookings:", data)

    app.run(debug=True)

