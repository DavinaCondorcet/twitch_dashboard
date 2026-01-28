import sqlite3
from pathlib import Path

DB_PATH = Path("data/valorant.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,
            date TEXT,
            agent TEXT,
            map TEXT,
            win INTEGER,
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            kda REAL,
            hs REAL,
            acs REAL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS rank_history (
            date TEXT,
            rank TEXT,
            rr INTEGER
        )
        """)

        conn.commit()
