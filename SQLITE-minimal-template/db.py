# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("app.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  start_date TEXT
);

CREATE TABLE IF NOT EXISTS costs(
  id INTEGER PRIMARY KEY,
  project_id INTEGER NOT NULL,
  item TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount >= 0),
  ts TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_costs_project_ts ON costs(project_id, ts);
"""

def connect(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    with connect() as conn:
        conn.executescript(SCHEMA)

def add_project(name, start_date=None):
    with connect() as conn:
        conn.execute("INSERT INTO projects(name, start_date) VALUES(?, ?)", (name, start_date))

def add_cost(project_id, item, amount, ts):
    with connect() as conn:
        conn.execute(
            "INSERT INTO costs(project_id, item, amount, ts) VALUES(?, ?, ?, ?)",
            (project_id, item, amount, ts)
        )

def list_costs(project_id):
    with connect() as conn:
        cur = conn.execute(
            "SELECT item, amount, ts FROM costs WHERE project_id=? ORDER BY ts",
            (project_id,)
        )
        return [dict(row) for row in cur]
