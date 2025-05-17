import sqlite3
from datetime import datetime
from pathlib import Path
from .config import BASE_CHAT_URL

DB_PATH = Path(__file__).parent.parent / "database" / "support.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    # Для удобства работы с dict и автокоммита
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'new',  -- new | active | archived
                created_at TEXT NOT NULL,
                taken_by TEXT  -- login оператора
            );
        """)

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
        return [(row["id"], generate_chat_url(user_id, row["id"])) for row in rows]

def generate_chat_url(user_id: int, ticket_id: int) -> str:
    return f"{BASE_CHAT_URL}/chat?uid={user_id}&ticket_id={ticket_id}"

def get_ticket_by_id(ticket_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_messages_by_ticket(ticket_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, content, timestamp FROM messages
            WHERE ticket_id = ? ORDER BY timestamp
        """, (ticket_id,))
        rows = cursor.fetchall()
        return [{"sender": r["sender"], "content": r["content"], "timestamp": r["timestamp"]} for r in rows]

def save_message(ticket_id, sender, text):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (ticket_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
            (ticket_id, sender or "user", text, datetime.utcnow().isoformat())
        )
        conn.commit()

def get_tickets_by_status(status):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, created_at
            FROM tickets
            WHERE status = ?
            ORDER BY created_at DESC
        """, (status,))
        return [dict(row) for row in cursor.fetchall()]
