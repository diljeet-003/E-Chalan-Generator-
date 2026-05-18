import sqlite3

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT,
        violation TEXT,
        fine INTEGER,
        location TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_challan(vehicle_no, violation, fine, location, date):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO challans(vehicle_no, violation, fine, location, date)
    VALUES (?, ?, ?, ?, ?)
    """, (vehicle_no, violation, fine, location, date))

    conn.commit()
    conn.close()