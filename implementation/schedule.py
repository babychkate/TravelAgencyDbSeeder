import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "schedules.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Вставка schedule_hours ---
schedule_hours = data.get("schedule_hours", [])
with conn.cursor() as cursor:
    added_count = 0
    for sh in schedule_hours:
        # Перевірка наявності години
        cursor.execute(
            "SELECT schedule_hours_id FROM schedule_hours WHERE schedule_arrival_time = ? AND schedule_departure_time = ?",
            sh["schedule_arrival_time"], sh["schedule_departure_time"]
        )
        if cursor.fetchone():
            continue

        # Вставка нової години
        cursor.execute(
            "INSERT INTO schedule_hours (schedule_arrival_time, schedule_departure_time) VALUES (?, ?)",
            sh["schedule_arrival_time"], sh["schedule_departure_time"]
        )
        added_count += 1
    conn.commit()
print(f"✅ Внесено {added_count} schedule_hours")

# --- 2. Вставка schedule_day ---
schedule_days = data.get("schedule_day", [])
with conn.cursor() as cursor:
    added_count = 0
    for sd in schedule_days:
        # Перевірка наявності дня
        cursor.execute(
            "SELECT schedule_day_id FROM schedule_day WHERE schedule_day_name = ?",
            sd["schedule_day_name"]
        )
        if cursor.fetchone():
            continue

        # Вставка нового дня
        cursor.execute(
            "INSERT INTO schedule_day (schedule_day_name) VALUES (?)",
            sd["schedule_day_name"]
        )
        added_count += 1
    conn.commit()
print(f"✅ Внесено {added_count} schedule_days")

# --- 3. Вставка schedule ---
schedule_list = data.get("schedule", [])
with conn.cursor() as cursor:
    added_count = 0
    for s in schedule_list:
        # Отримуємо schedule_day_id
        cursor.execute(
            "SELECT schedule_day_id FROM schedule_day WHERE schedule_day_name = ?",
            s["schedule_day_name"]
        )
        day_row = cursor.fetchone()
        if not day_row:
            continue
        schedule_day_id = day_row[0]

        # Отримуємо schedule_hours_id
        cursor.execute(
            "SELECT schedule_hours_id FROM schedule_hours WHERE schedule_arrival_time = ? AND schedule_departure_time = ?",
            s["schedule_arrival_time"], s["schedule_departure_time"]
        )
        hour_row = cursor.fetchone()
        if not hour_row:
            continue
        schedule_hours_id = hour_row[0]

        # Перевірка чи такий запис вже існує
        cursor.execute(
            "SELECT schedule_id FROM schedule WHERE schedule_day_id = ? AND schedule_hours_id = ?",
            schedule_day_id, schedule_hours_id
        )
        if cursor.fetchone():
            continue

        # Вставка в schedule
        cursor.execute(
            "INSERT INTO schedule (schedule_day_id, schedule_hours_id) VALUES (?, ?)",
            schedule_day_id, schedule_hours_id
        )
        added_count += 1
    conn.commit()
print(f"✅ Внесено {added_count} schedule")
