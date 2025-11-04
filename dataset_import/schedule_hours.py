import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "schedule_hours.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Беремо всі записи з одного масиву "schedule hours"
schedule_hours = data.get("schedule hours", [])

with conn.cursor() as cursor:
    for sh in schedule_hours:
        cursor.execute("""
            INSERT INTO schedule_hours (schedule_departure_time, schedule_arrival_time)
            VALUES (?, ?)
        """, (sh["schedule_departure_time"], sh["schedule_arrival_time"]))
    conn.commit()

print(f"✅ Внесено {len(schedule_hours)} schedule hours")
