import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "season_schedules.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

bus_schedules = data.get("bus trip season schedules", [])
flight_schedules = data.get("flight season schedules", [])

with conn.cursor() as cursor:
    # --- Bus Trip Season Schedules ---
    for sched in bus_schedules:
        # Отримуємо bus_trip_season_id
        cursor.execute("""
            SELECT bus_trip_season_id
            FROM bus_trip_season bts
            JOIN bus_trip_route btr ON bts.bus_trip_route_id = btr.bus_trip_route_id
            WHERE btr.route_number = ? AND bts.bus_trip_season_start_date = ? AND bts.bus_trip_season_end_date = ?
        """, (sched["route_number"], sched["season_start_date"], sched["season_end_date"]))
        season_id_row = cursor.fetchone()
        if not season_id_row:
            continue
        season_id = season_id_row[0]

        # Отримуємо schedule_id
        cursor.execute("""
            SELECT sh.schedule_hours_id, sd.schedule_day_id, s.schedule_id
            FROM schedule s
            JOIN schedule_hours sh ON s.schedule_hours_id = sh.schedule_hours_id
            JOIN schedule_day sd ON s.schedule_day_id = sd.schedule_day_id
            WHERE sh.schedule_departure_time = ? AND sh.schedule_arrival_time = ?
              AND sd.schedule_day_name = ?
        """, (sched["schedule_departure_time"], sched["schedule_arrival_time"], sched["schedule_day_name"]))
        schedule_row = cursor.fetchone()
        if not schedule_row:
            continue
        schedule_id = schedule_row[2]

        # Перевірка дублікату
        cursor.execute("""
            SELECT 1
            FROM bus_trip_season_schedule
            WHERE bus_trip_season_id = ? AND schedule_id = ?
        """, (season_id, schedule_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO bus_trip_season_schedule (bus_trip_season_id, schedule_id)
                VALUES (?, ?)
            """, (season_id, schedule_id))

    # --- Flight Season Schedules ---
    for sched in flight_schedules:
        # Отримуємо flight_season_id
        cursor.execute("""
            SELECT flight_season_id
            FROM flight_season fs
            JOIN flight_route fr ON fs.flight_route_id = fr.flight_route_id
            WHERE fr.route_number = ? AND fs.flight_season_start_date = ? AND fs.flight_season_end_date = ?
        """, (sched["route_number"], sched["season_start_date"], sched["season_end_date"]))
        season_id_row = cursor.fetchone()
        if not season_id_row:
            continue
        season_id = season_id_row[0]

        # Отримуємо schedule_id
        cursor.execute("""
            SELECT sh.schedule_hours_id, sd.schedule_day_id, s.schedule_id
            FROM schedule s
            JOIN schedule_hours sh ON s.schedule_hours_id = sh.schedule_hours_id
            JOIN schedule_day sd ON s.schedule_day_id = sd.schedule_day_id
            WHERE sh.schedule_departure_time = ? AND sh.schedule_arrival_time = ?
              AND sd.schedule_day_name = ?
        """, (sched["schedule_departure_time"], sched["schedule_arrival_time"], sched["schedule_day_name"]))
        schedule_row = cursor.fetchone()
        if not schedule_row:
            continue
        schedule_id = schedule_row[2]

        # Перевірка дублікату
        cursor.execute("""
            SELECT 1
            FROM flight_season_schedule
            WHERE flight_season_id = ? AND schedule_id = ?
        """, (season_id, schedule_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO flight_season_schedule (flight_season_id, schedule_id)
                VALUES (?, ?)
            """, (season_id, schedule_id))

    conn.commit()

print(f"✅ Внесено {len(bus_schedules)} bus trip season schedules та {len(flight_schedules)} flight season schedules")
