import sqlite3

db_name = "lines.db"


def lines_init():
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS lines (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   uid INTEGER,
                   email TEXT UNIQUE)""")
    conn.commit()
    conn.close()


def lines_clear():
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM lines""")
    conn.commit()
    conn.close()


def del_lines(uid):
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM lines WHERE uid = ?""", (uid,))
    conn.commit()
    conn.close()


def add_line(uid, email):
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    try:

        cursor.execute(
            """INSERT INTO lines (uid, email) VALUES (?, ?)""", (uid, email))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def request_lines(uid):
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute("""SELECT email FROM lines WHERE uid = ?""", (uid,))
    userlines = cursor.fetchall()
    conn.close()
    return [row[0] for row in userlines]
