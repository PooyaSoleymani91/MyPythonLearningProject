import sqlite3
from pathlib import Path

DB_PATH = Path("WMSapp.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS anbarha(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  isactive BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  PrimaryVahed TEXT NOT NULL,
  SeconderyVahed TEXT,
  ConvertionRatioPtoS NUMERIC(10,4),
  isconsumables BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS Tajhizat(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code_amval TEXT NOT NULL,
  anbar_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  isintact BOOLEAN NOT NULL,
  Qtyx1000 INTEGER CHECK(Qtyx1000 >= 0), 
  FOREIGN KEY(anbar_id) REFERENCES anbarha(id) ON DELETE CASCADE,
  FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
  UNIQUE(code_amval, anbar_id)
);

CREATE TABLE IF NOT EXISTS masrafi(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  anbar_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  crntQty INTEGER CHECK(crntQty >= 0),
  FOREIGN KEY(anbar_id) REFERENCES anbarha(id) ON DELETE CASCADE,
  FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tbl_transaction(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  rsntlybght BOOLEAN NOT NULL,
  sourceAnbar_id INTEGER NOT NULL,
  destAnbar_id INTEGER NOT NULL,
  datetr TEXT NOT NULL,
  isadd BOOLEAN NOT NULL,
  Qtyadd INTEGER CHECK( (isadd = 1 AND Qtyadd >= 0 AND Qtysub = 0) OR (isadd = 0 AND Qtysub >= 0 AND Qtyadd = 0) ),
  Qtysub INTEGER CHECK((Qtysub >= 0) AND ((Qtyadd - Qtysub) >= 0) AND (isadd = 0))
);

CREATE TABLE IF NOT EXISTS persons(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  familyname TEXT NOT NULL,
  personalcode TEXT NOT NULL
);
"""

SQLTRIGERS="""
  CREATE TRIGGER IF NOT EXISTS trg_update_masrafi
AFTER INSERT ON tbl_transaction
FOR EACH ROW
BEGIN
    -- اگر تراکنش اضافه کردن بود
    UPDATE masrafi
    SET crntQty = crntQty + NEW.Qtyadd
    WHERE anbar_id = NEW.destAnbar_id
      AND item_id = NEW.item_id;

    -- اگر هیچ رکوردی برای این انبار و آیتم نبود، رکورد جدید بساز
    INSERT INTO masrafi (anbar_id, item_id, crntQty)
    SELECT NEW.destAnbar_id, NEW.item_id, NEW.Qtyadd
    WHERE NOT EXISTS (
        SELECT 1 FROM masrafi
        WHERE anbar_id = NEW.destAnbar_id
          AND item_id = NEW.item_id
    );
END;

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
        conn.executescript(SQLTRIGERS)

def add_anbar(name):
    try:
        with connect() as conn:
            cur=conn.execute("INSERT INTO anbarha(name,isactive) VALUES(?,?)", (name,True))
            conn.commit()  # برای ذخیره تغییرات
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("این نام قبلاً ثبت شده است")
        return None

def add_item(name,primVahed,secVahed,convRt,iscons):
    try:
        with connect() as conn:
            cur=conn.execute("INSERT INTO items(name,Primaryvahed,SeconderyVahed,ConvertionRatioPtoS,isconsumables) VALUES(?,?,?,?,?)",
            (name,primVahed,secVahed,convRt,iscons))
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        print("این جنس قبلاً ثبت شده است")
        return None
    
def add_trns(item_id,rsntlybght,sourceAnbar_id,destAnbar_id,datetr,isadd,Qtyadd,Qtysub):
    try:
        with connect() as conn:
            cur=conn.execute("INSERT INTO tbl_transaction(item_id,rsntlybght,sourceAnbar_id,destAnbar_id,datetr,isadd,Qtyadd,Qtysub) VALUES(?,?,?,?,?,?,?,?)",
            (item_id,rsntlybght,sourceAnbar_id,destAnbar_id,datetr,isadd,Qtyadd,Qtysub))
            conn.commit()
            return cur.lastrowid
    except :
        print("خطا!")
        return None

def add_update_Tajhizat():
    print()