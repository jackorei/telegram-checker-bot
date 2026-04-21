import sqlite3

db_name = "kitty.db"


def init_db():
    """Run this once to create the vault."""
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS hits (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   uid INTEGER, 
                   email TEXT UNIQUE, 
                   status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def clear_db():
    """Run this once to clear the vault."""
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM hits''')
    conn.commit()
    conn.close()


def add_hit(uid, email, status):
    """Saves a result. If the email exists, it updates the status."""
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''INSERT INTO hits (uid, email, status) VALUES (?, ?, ?) ON CONFLICT(email) DO UPDATE SET status=excluded.status''', (uid, email, status))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def get_hits(uid):
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT email FROM hits WHERE uid = ? AND status = ?''', (uid, "Good",))
    allhits = cursor.fetchall()
    conn.close()
    return allhits


def get_stats():
    """Returns a count of all hits."""
    conn = sqlite3.connect(db_name, timeout=20)
    cursor = conn.cursor()
    conn.execute(''' SELECT COUNT(*) FROM hits''')
    count = cursor.fetchone()[0]
    conn.close()
    return count
