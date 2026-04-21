import sqlite3
import secrets

db_name = "license.db"


def init_license():
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS license (id INTEGER PRIMARY KEY AUTOINCREMENT, code INTEGER, uid INTEGER)""")
    conn.commit()
    conn.close()


def add_license():
    token = secrets.token_hex(12)
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO license (code, uid) VALUES (?, ?)""", (token, 0))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def user_license(uid, code):
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE license SET uid = ? WHERE code = ?""", (uid, code))
    conn.commit()
    conn.close()


def clear_license():
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM license """)
    conn.commit()
    conn.close()


def get_license():
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT code FROM license""")
    licenses = cursor.fetchall()
    conn.close()
    return licenses


def find_license(key):
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM license WHERE code = ? AND uid = ?)""", (key, 0))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def license_exists(key):
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM license WHERE code = ?)""", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def is_registered(uid):
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT EXISTS (SELECT 1 FROM license WHERE uid = ?)""", (uid,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def revoke_license(code):
    conn = sqlite3.connect(db_name, timeout=10)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM license WHERE code = ?""", (code,))
    conn.commit()
    conn.close()
