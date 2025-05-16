import sqlite3
from datetime import datetime
from pathlib import Path
from .config import BASE_CHAT_URL

DB_PATH = Path(__file__).parent.parent / "database" / "support.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Таблица обращений
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'new',  -- new | active | archived
                created_at TEXT NOT NULL,
                taken_by TEXT  -- login оператора
            );
        """)

        # Таблица сообщений (пока не используется, но заложена на будущее)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                sender TEXT NOT NULL,  -- 'user' или 'operator'
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            );
        """)

        conn.commit()

def create_ticket(user_id: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (user_id, status, created_at)
            VALUES (?, 'new', ?)
        """, (user_id, datetime.utcnow().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_archived_tickets(user_id: int) -> list[tuple[int, str]]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM tickets
            WHERE user_id = ? AND status = 'archived'
            ORDER BY created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        return [(row[0], generate_chat_url(user_id, row[0])) for row in rows]

def generate_chat_url(user_id: int, ticket_id: int) -> str:
    return f"{BASE_CHAT_URL}/chat?uid={user_id}&ticket_id={ticket_id}"

