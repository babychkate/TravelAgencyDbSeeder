import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Bus Trip Seasons ---
bus_trip_seasons = data.get("bus trip seasons", [])

with conn.cursor() as cursor:
    added_count = 0
    for season in bus_trip_seasons:
        # Отримуємо bus_trip_route_id по route_number
        cursor.execute(
            "SELECT bus_trip_route_id FROM bus_trip_route WHERE route_number = ?",
            season["route_number"]
        )
        route_row = cursor.fetchone()
        if not route_row:
            continue
        bus_trip_route_id = route_row[0]

        # Вставка у bus_trip_season
        cursor.execute(
            """
            INSERT INTO bus_trip_season
            (bus_trip_route_id, bus_trip_season_start_date, bus_trip_season_end_date)
            VALUES (?, ?, ?)
            """,
            bus_trip_route_id,
            season["bus_trip_season_start_date"],
            season["bus_trip_season_end_date"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} bus_trip_seasons")

# --- 2. Flight Seasons ---
flight_seasons = data.get("flight seasons", [])

with conn.cursor() as cursor:
    added_count = 0
    for season in flight_seasons:
        # Отримуємо flight_route_id по route_number
        cursor.execute(
            "SELECT flight_route_id FROM flight_route WHERE route_number = ?",
            season["route_number"]
        )
        route_row = cursor.fetchone()
        if not route_row:
            continue
        flight_route_id = route_row[0]

        # Вставка у flight_season
        cursor.execute(
            """
            INSERT INTO flight_season
            (flight_route_id, flight_season_start_date, flight_season_end_date)
            VALUES (?, ?, ?)
            """,
            flight_route_id,
            season["flight_trip_season_start_date"],
            season["flight_trip_season_end_date"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} flight_seasons")
