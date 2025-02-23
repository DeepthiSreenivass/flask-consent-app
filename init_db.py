import sqlite3

DATABASE = "participants.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                phone_number TEXT,
                consent_date TEXT
            )
        ''')
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
