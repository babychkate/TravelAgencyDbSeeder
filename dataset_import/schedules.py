import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "schedules.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

schedules = data.get("schedules", [])

with conn.cursor() as cursor:
    for s in schedules:
        # --- Отримуємо schedule_hours_id ---
        cursor.execute("""
            SELECT schedule_hours_id 
            FROM schedule_hours 
            WHERE schedule_departure_time = ? AND schedule_arrival_time = ?
        """, (s["schedule_departure_time"], s["schedule_arrival_time"]))
        hours_id = cursor.fetchone()
        if not hours_id:
            continue
        hours_id = hours_id[0]

        # --- Отримуємо schedule_day_id ---
        cursor.execute("""
            SELECT schedule_day_id 
            FROM schedule_day 
            WHERE schedule_day_name = ?
        """, (s["schedule_day_name"],))
        day_id = cursor.fetchone()
        if not day_id:
            continue
        day_id = day_id[0]

        # --- Вставка в schedule ---
        cursor.execute("""
            INSERT INTO schedule (schedule_hours_id, schedule_day_id)
            VALUES (?, ?)
        """, (hours_id, day_id))
    conn.commit()

print(f"✅ Внесено {len(schedules)} schedules")
