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
  vahed TEXT,
  bahayeVahed INTEGER,
  FOREIGN KEY(fehrestbaha_id) REFERENCES fehrestbaha(id) ON DELETE CASCADE
  UNIQUE(itemCode, fehrestbaha_id)
);

CREATE INDEX IF NOT EXISTS idx_items_fehrestbaha ON items(fehrestbaha_id);
"""
# ON DELETE CASCADE -> if i delete a fehrestbaha then items of it will deleted too



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
    try:
        with connect() as conn:
            cur=conn.execute("INSERT INTO fehrestbaha(name) VALUES(?)", (name,))
            conn.commit()  # برای ذخیره تغییرات
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("این نام قبلاً ثبت شده است")
        return None

def add_items(itemCode,fehrestbaha_id, item, vahed, bahayeVahed):
    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO items(itemCode,fehrestbaha_id, item, vahed, bahayeVahed) VALUES(?, ?, ?, ?, ?)",
                (itemCode,fehrestbaha_id, item, vahed, bahayeVahed)
            )
            conn.commit()# برای ذخیره تغییرات
    except sqlite3.IntegrityError:
        print("این نام قبلاً ثبت شده است")
        return None    

def list_items(fehrestbaha_id):
    with connect() as conn:
        cur = conn.execute(
            "SELECT itemCode , item, vahed, bahayeVahed FROM items WHERE fehrestbaha_id=? ORDER BY itemCode",
            (fehrestbaha_id,)
        )
        return [dict(row) for row in cur]

def list_fehrestbaha():
    with connect() as conn:
        cur =conn.execute(
            "SELECT id, name FROM fehrestbaha ORDER BY id",
        )
        return [dict(row) for row in cur]

def show_item(fehrestbaha_name, itemc):
    init_db()
    allFbs=list_fehrestbaha()
    for fbs in allFbs:
        if fbs["name"]==fehrestbaha_name:
            fehrestbaha_id=fbs["id"]
    with connect() as conn:
        cur = conn.execute(
            "SELECT itemCode, item, vahed, bahayeVahed "
            "FROM items "
            "WHERE fehrestbaha_id=? AND itemCode=? "
            "ORDER BY itemCode",
            (fehrestbaha_id, itemc) #be jaye alamat soal ha(?) be tatrib fehrestbaba_id , itemc mizare
        )
        return [dict(row) for row in cur]

def delete_all_itemsdb(fehrestbaha_name):
    init_db()
    allFbs = list_fehrestbaha()
    fehrestbaha_id = None
    for fbs in allFbs:
        if fbs["name"] == fehrestbaha_name:
            fehrestbaha_id = fbs["id"]
            break
    if fehrestbaha_id is None:
        raise ValueError(f"Fehrestbaha '{fehrestbaha_name}' not found")
    with connect() as conn:
        conn.execute("DELETE FROM fehrestbaha WHERE id=?", (fehrestbaha_id,))
        conn.commit()