import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .config import get_settings

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS conversations (
 id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
 id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL,
 role TEXT NOT NULL CHECK(role IN ('user','assistant','system')),
 content TEXT NOT NULL, created_at TEXT NOT NULL,
 FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, id);
CREATE TABLE IF NOT EXISTS memories (
 id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, content TEXT NOT NULL,
 sha256 TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL
);
"""

def connect():
    path = Path(get_settings().database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    with connect() as conn:
        conn.executescript(SCHEMA)

@contextmanager
def db():
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
