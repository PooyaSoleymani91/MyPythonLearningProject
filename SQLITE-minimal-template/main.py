from datetime import datetime
from db import init_db, add_project, add_cost, list_costs

init_db()
add_project("پروژه A", "2025-08-01")
now = datetime.now().isoformat(timespec="seconds")
add_cost(1, "هزینه اولیه", 5000, now)
print(list_costs(1))
