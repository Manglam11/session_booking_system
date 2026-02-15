import sqlite3
from services.logger_config import logger


DB_NAME = "database/database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database ready.")


def add_booking(name, email, date, time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE date=? AND time=?",
        (date, time)
    )

    if cursor.fetchone():
        conn.close()
        logger.warning(f"Slot already booked for {date} {time}")
        return False

    cursor.execute(
        "INSERT INTO bookings (name, email, date, time) VALUES (?, ?, ?, ?)",
        (name, email, date, time)
    )

    conn.commit()
    conn.close()

    logger.info(f"Booking created for {email} on {date} {time}")
    return True


def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    conn.close()
    return rows
