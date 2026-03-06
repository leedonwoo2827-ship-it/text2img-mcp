# -*- coding: utf-8 -*-
import sqlite3
import uuid
from pathlib import Path

DEFAULT_DB_DIR = Path.home() / "Documents" / "text2img-mcp"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "history.db"


def _get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    conn = _get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id TEXT PRIMARY KEY,
            prompt TEXT NOT NULL,
            image_path TEXT NOT NULL,
            aspect_ratio TEXT DEFAULT '1:1',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_generation(prompt: str, image_path: str, aspect_ratio: str = "1:1",
                     db_path: Path = DEFAULT_DB_PATH) -> str:
    gen_id = str(uuid.uuid4())
    conn = _get_connection(db_path)
    conn.execute(
        "INSERT INTO generations (id, prompt, image_path, aspect_ratio) VALUES (?, ?, ?, ?)",
        (gen_id, prompt, image_path, aspect_ratio),
    )
    conn.commit()
    conn.close()
    return gen_id


def get_generations(limit: int = 50, db_path: Path = DEFAULT_DB_PATH) -> list[dict]:
    conn = _get_connection(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM generations ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
