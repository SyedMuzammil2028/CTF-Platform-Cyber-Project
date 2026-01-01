
import os
import sqlite3
from config import DB_PATH

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table (for SQLi, auth brute-force, CSRF-ish stuff)
    c.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT,
        flag TEXT
    )""")

    users = [
        ("guest", "guest123", "user", "guest@example.com", None),
        ("testuser", "test123", "user", "test@example.com", None),
        ("muzammil", "slayer123", "user", "muzammil@example.com", None),
        ("admin", "SuperSecure!@#", "admin", "admin@deathnote.local", "DNCTF{sqli_admin_l0gin}"),
        ("weakadmin", "password123", "admin", "weakadmin@deathnote.local", "DNCTF{brut3_f0rc3_w1ns}"),
        ("csrf_victim", "victim123", "admin", "victim@deathnote.local", "DNCTF{csrf_st0len_st4te}"),
    ]
    c.executemany(
        "INSERT INTO users (username, password, role, email, flag) VALUES (?, ?, ?, ?, ?)",
        users,
    )

    # Secrets table (for SQLi UNION)
    c.execute("""CREATE TABLE secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        note TEXT NOT NULL,
        flag TEXT NOT NULL
    )""")

    secrets = [
        ("admin", "Kira's hidden note", "DNCTF{sqli_union_owns_the_note}"),
        ("muzammil", "Just a practice secret", "DNCTF{dummy_secret_1}"),
        ("guest", "Nothing special here", "DNCTF{dummy_secret_2}"),
    ]
    c.executemany(
        "INSERT INTO secrets (owner, note, flag) VALUES (?, ?, ?)",
        secrets,
    )

    # Profiles table (for IDOR)
    c.execute("""CREATE TABLE profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        display_name TEXT NOT NULL,
        bio TEXT NOT NULL,
        is_admin INTEGER NOT NULL,
        flag TEXT
    )""")

    profiles = [
        ("guest", "Guest User", "Just exploring...", 0, None),
        ("testuser", "Test User", "Loves testing things.", 0, None),
        ("muzammil", "Muzammil", "Web slayer.", 0, None),
    ]

    for i in range(4, 101):
        profiles.append((
            f"user{i}",
            f"User {i}",
            "Nothing interesting here.",
            0,
            None,
        ))

    profiles.append((
        "hidden_admin",
        "Kira",
        "The god of the new world.",
        1,
        "DNCTF{idor_unl0ck3d_101}",
    ))

    c.executemany(
        "INSERT INTO profiles (username, display_name, bio, is_admin, flag) VALUES (?, ?, ?, ?, ?)",
        profiles,
    )

    # Comments table (Stored XSS)
    c.execute("""CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )""")

    c.execute("INSERT INTO comments (content) VALUES (?)", ("First blood...",))

    conn.commit()
    conn.close()
    print("Database initialized at", DB_PATH)


if __name__ == "__main__":
    init_db()
