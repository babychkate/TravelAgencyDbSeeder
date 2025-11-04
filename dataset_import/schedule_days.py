import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "schedule_days.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    schedule_days = data.get("schedule days", [])

with conn.cursor() as cursor:
    for day in schedule_days:
        cursor.execute("""
            INSERT INTO schedule_day (schedule_day_name)
            VALUES (?)
        """, (day["schedule_day_name"],))
    conn.commit()

print(f"✅ Внесено {len(schedule_days)} schedule days")
