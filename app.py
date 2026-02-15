import sqlite3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is my first Flask app!"

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
    print(cursor.fetchall())
    conn.commit()
    conn.close()
    print("Table created successfully.")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)

