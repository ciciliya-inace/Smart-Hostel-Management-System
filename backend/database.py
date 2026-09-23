import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "hostel.db")


def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            leave_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()