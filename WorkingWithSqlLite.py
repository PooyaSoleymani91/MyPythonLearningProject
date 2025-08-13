import sqlite3
from pathlib import Path



##DataBase Creatation Steps:
#Step0: define path using pathlib
DB_PATH = Path("app.db") 

#Step1: Secure connection + basic settings
def connect(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row                 #output like dictionaries
    conn.execute("PRAGMA foreign_keys = ON;")      #Enable Foregin keys
    return conn
#
# الگوی استاندارد استفاده (اتوماتیک commit/rollback و بستن اتصال)
with connect() as conn:
    conn.execute("PRAGMA journal_mode = WAL;")     # Improved synchronization and speed
#WAL improves multiple reading speed for desktop-app and single-users app

#ُStep2: Making tables: (Schema):
schema_sql = """
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    start_date  TEXT
);

CREATE TABLE IF NOT EXISTS costs (
    id          INTEGER PRIMARY KEY,
    project_id  INTEGER NOT NULL,
    item        TEXT NOT NULL,
    amount      REAL NOT NULL CHECK(amount >= 0),
    ts          TEXT NOT NULL,                     -- ISO datetime
    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Indexes******
CREATE INDEX IF NOT EXISTS idx_costs_project ON costs(project_id);
CREATE INDEX IF NOT EXISTS idx_costs_ts      ON costs(ts);
"""
# ****** "--" >>>>> this is for commenting in sqlite language
with connect() as conn:
    conn.executescript(schema_sql)

#Step3: Insert data - Secure and fast:

from datetime import datetime

with connect() as conn:
    conn.execute("INSERT INTO projects(name, start_date) VALUES(?, ?)",
                 ("خط لوله شمال", "2025-08-01"))

    now = datetime.now().isoformat(timespec="seconds")
    rows = [
        (1, "خاکبرداری", 12000.0, now),
        (1, "لوله‌گذاری", 35000.0, now),
        (1, "ایاب‌وذهاب", 1800.0,  now),
    ]
    conn.executemany(
        "INSERT INTO costs(project_id, item, amount, ts) VALUES(?, ?, ?, ?)",
        rows
    )

#Step4: Select(Read) Data as dictionary:
with connect() as conn:
    cur = conn.execute("SELECT id, name, start_date FROM projects")
    for row in cur:
        print(row["id"], row["name"], row["start_date"])

#Step5: Update and delete data:
with connect() as conn:
    conn.execute("UPDATE costs SET amount = amount * 1.1 WHERE item = ?", ("خاکبرداری",))
    conn.execute("DELETE FROM costs WHERE amount < ?", (2000,))

#Step6: Join and report (Aggregation):
report_sql = """
SELECT p.name AS project,
       COUNT(c.id)  AS cost_items,
       SUM(c.amount) AS total_amount
FROM projects p
LEFT JOIN costs c ON c.project_id = p.id
GROUP BY p.id
ORDER BY total_amount DESC;
"""
with connect() as conn:
    for row in conn.execute(report_sql):
        print(f"{row['project']}: {row['cost_items']} آیتم، جمع {row['total_amount']}")

#Step7:Bulk import - One big transaction is much faster than multiple small ones:
#One transaction = much faster + guaranteed atomicity
def bulk_add_costs(project_id, rows):
    """
    rows: iterable of (item, amount, ts_text)
    """
    with connect() as conn:
        conn.executemany(
            "INSERT INTO costs(project_id, item, amount, ts) VALUES(?, ?, ?, ?)",
            ((project_id, it, am, ts) for (it, am, ts) in rows)
        )

# How to use:
from datetime import datetime, timedelta
base = datetime.now().replace(microsecond=0)
rows = [(f"هزینه-{i}", float(i)*1000, (base).isoformat()) for i in range(1, 501)]
bulk_add_costs(1, rows)
