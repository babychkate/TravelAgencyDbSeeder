import json
from pathlib import Path
from sql_connection import conn

file_path = Path(__file__).parent.parent / "data" / "season_schedules.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

bus_schedules = data.get("bus trip season schedules", [])
flight_schedules = data.get("flight season schedules", [])

with conn.cursor() as cursor:
    added_bus = 0
    added_flight = 0

    # --- BUS SCHEDULES ---
    for bs in bus_schedules:
        # Знаходимо bus_trip_season_id
        cursor.execute(
            """
            SELECT bus_trip_season_id
            FROM bus_trip_season bts
            JOIN bus_trip_route btr ON bts.bus_trip_route_id = btr.bus_trip_route_id
            WHERE btr.route_number = ?
              AND bts.bus_trip_season_start_date = ?
              AND bts.bus_trip_season_end_date = ?
            """,
            bs["route_number"],
            bs["bus_trip_season_start_date"],
            bs["bus_trip_season_end_date"]
        )
        season_row = cursor.fetchone()
        if not season_row:
            print(f"⚠️ Пропущено: не знайдено bus_trip_season для маршруту {bs['route_number']}")
            continue
        bus_trip_season_id = season_row[0]

        # Знаходимо schedule_id
        cursor.execute(
            """
            SELECT schedule_id
            FROM schedule s
            JOIN schedule_day sd ON s.schedule_day_id = sd.schedule_day_id
            JOIN schedule_hours sh ON s.schedule_hours_id = sh.schedule_hours_id
            WHERE sd.schedule_day_name = ?
              AND sh.schedule_departure_time = ?
              AND sh.schedule_arrival_time = ?
            """,
            bs["day_name"],
            bs["schedule_departure_time"],
            bs["schedule_arrival_time"]
        )
        schedule_row = cursor.fetchone()
        if not schedule_row:
            print(f"⚠️ Пропущено: не знайдено schedule для {bs['day_name']} {bs['schedule_departure_time']}-{bs['schedule_arrival_time']}")
            continue
        schedule_id = schedule_row[0]

        # Вставка у проміжну таблицю
        cursor.execute(
            "INSERT INTO bus_trip_season_schedule (bus_trip_season_id, schedule_id) VALUES (?, ?)",
            bus_trip_season_id, schedule_id
        )
        added_bus += 1

    # --- FLIGHT SCHEDULES ---
    for fs in flight_schedules:
        # Знаходимо flight_season_id
        cursor.execute(
            """
            SELECT flight_season_id
            FROM flight_season fs
            JOIN flight_route fr ON fs.flight_route_id = fr.flight_route_id
            WHERE fr.route_number = ?
              AND fs.flight_season_start_date = ?
              AND fs.flight_season_end_date = ?
            """,
            fs["route_number"],
            fs["flight_trip_season_start_date"],
            fs["flight_trip_season_end_date"]
        )
        season_row = cursor.fetchone()
        if not season_row:
            print(f"⚠️ Пропущено: не знайдено flight_season для маршруту {fs['route_number']}")
            continue
        flight_season_id = season_row[0]

        # Знаходимо schedule_id
        cursor.execute(
            """
            SELECT schedule_id
            FROM schedule s
            JOIN schedule_day sd ON s.schedule_day_id = sd.schedule_day_id
            JOIN schedule_hours sh ON s.schedule_hours_id = sh.schedule_hours_id
            WHERE sd.schedule_day_name = ?
              AND sh.schedule_departure_time = ?
              AND sh.schedule_arrival_time = ?
            """,
            fs["day_name"],
            fs["schedule_departure_time"],
            fs["schedule_arrival_time"]
        )
        schedule_row = cursor.fetchone()
        if not schedule_row:
            print(f"⚠️ Пропущено: не знайдено schedule для {fs['day_name']} {fs['schedule_departure_time']}-{fs['schedule_arrival_time']}")
            continue
        schedule_id = schedule_row[0]

        # Вставка у проміжну таблицю
        cursor.execute(
            "INSERT INTO flight_season_schedule (flight_season_id, schedule_id) VALUES (?, ?)",
            flight_season_id, schedule_id
        )
        added_flight += 1

    conn.commit()

print(f"✅ Внесено {added_bus} записів у bus_trip_season_schedule")
print(f"✅ Внесено {added_flight} записів у flight_season_schedule")
