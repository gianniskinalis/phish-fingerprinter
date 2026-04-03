Should i do this for all other projects?import sqlite3
import json
from datetime import datetime

DB_FILE = "phish.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            sha256 TEXT,
            forms TEXT,
            emails TEXT,
            kit_family TEXT,
            collected_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[+] Database initialized")


def save_page(url, title, sha256, forms, emails, kit_family):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT id FROM pages WHERE sha256 = ?", (sha256,))
    existing = c.fetchone()
    if existing:
        print(f"  [!] Skipping duplicate: {title}")
        conn.close()
        return

    c.execute("""
        INSERT INTO pages (url, title, sha256, forms, emails, kit_family, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        url,
        title,
        sha256,
        json.dumps(forms),
        json.dumps(emails),
        kit_family,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def show_all():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM pages")
    rows = c.fetchall()
    conn.close()

    print("\n[+] {len(rows)} pages in database\n")
    for row in rows:
        print(f"  ID:  {row[0]}")
        print(f"  URL:  {row[1]}")
        print(f"  Title:  {row[2]}")
        print(f"  SHA256:  {row[3]}")
        print(f"  Forms:  {row[4]}")
        print(f"  Emails:  {row[5]}")
        print(f"  Kit Family:  {row[6]}")
        print(f"  Collected: {row[7]}")
        print()


def show_families():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT kit_family, COUNT(*) as count FROM pages GROUP BY kit_family")
    rows = c.fetchall()
    conn.close()

    print(f"\n[+] Kit families in database\n")
    for row in rows:
        print(f"  {row[0]} - {row[1]} page(s)")


if __name__ == "__main__":
    init_db()
    show_all()
    show_families()

