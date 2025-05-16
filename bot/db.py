import sqlite3
from datetime import datetime
from pathlib import Path
from .config import BASE_DIR

DB_PATH = BASE_DIR / "database" / "support.db"
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL,
                taken_by TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            );
        """)

        conn.commit()

def create_ticket(user_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (user_id, status, created_at)
            VALUES (?, 'new', ?)
        """, (user_id, datetime.utcnow().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_ticket_by_id(ticket_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        return cursor.fetchone()

def get_messages_by_ticket(ticket_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sender, content, content_type, timestamp 
            FROM messages 
            WHERE ticket_id = ? 
            ORDER BY timestamp
        """, (ticket_id,))
        
        messages = []
        for row in cursor.fetchall():
            message = dict(row)
            if row['content_type'] in ['image', 'video']:
                message['content_url'] = f"/uploads/{row['content']}"
            messages.append(message)
            
        return messages

def save_message(ticket_id, sender, content, content_type):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages 
            (ticket_id, sender, content, content_type, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            sender,
            content,
            content_type,
            datetime.utcnow().isoformat()
        ))
        conn.commit()