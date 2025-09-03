import sqlite3
from pathlib import Path

DB_PATH = Path("appexcle.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS fehrestbaha(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS items(
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  itemCode TEXT NOT NULL,
  fehrestbaha_id INTEGER NOT NULL,
  item TEXT NOT NULL,
  vahed TEXT NOT NULL DEFAULT 'نامشخص',
  bahayeVahed INTEGER,
  FOREIGN KEY(fehrestbaha_id) REFERENCES fehrestbaha(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_items_fehrestbaha ON items(fehrestbaha_id);
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

def add_fehrestbaha(name):
    with connect() as conn:
        cur=conn.execute("INSERT INTO fehrestbaha(name) VALUES(?)", (name,))
        conn.commit()  # برای ذخیره تغییرات
        return cur.lastrowid

def add_items(itemCode,fehrestbaha_id, item, vahed, bahayeVahed):
    with connect() as conn:
        conn.execute(
            "INSERT INTO items(itemCode,fehrestbaha_id, item, vahed, bahayeVahed) VALUES(?, ?, ?, ?, ?)",
            (itemCode,fehrestbaha_id, item, vahed, bahayeVahed)
        )
        conn.commit()# برای ذخیره تغییرات

def list_items(fehrestbaha_id):
    with connect() as conn:
        cur = conn.execute(
            "SELECT itemCode , item, vahed, bahayeVahed FROM items WHERE fehrestbaha_id=? ORDER BY itemCode",
            (fehrestbaha_id,)
        )
        return [dict(row) for row in cur]
def list_fehrestbaha() -> dict:
    with connect() as conn:
        cur =conn.execute(
            "SELECT id, name FROM fehrestbaha ORDER BY id",
        )
        return [dict(row) for row in cur]

def show_item(fehrestbaha_id, itemc):
    with connect() as conn:
        cur = conn.execute(
            "SELECT itemCode, item, vahed, bahayeVahed "
            "FROM items "
            "WHERE fehrestbaha_id=? AND itemCode=? "
            "ORDER BY itemCode",
            (fehrestbaha_id, itemc) #be jaye alamat soal ha(?) be tatrib fehrestbaba_id , itemc mizare
        )
        return [dict(row) for row in cur]