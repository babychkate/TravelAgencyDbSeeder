import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

bus_trip_seasons = data.get("bus trip seasons", [])
flight_seasons = data.get("flight seasons", [])

with conn.cursor() as cursor:
    # --- Bus trip seasons ---
    for season in bus_trip_seasons:
        cursor.execute("""
            SELECT bus_trip_route_id
            FROM bus_trip_route
            WHERE route_number = ?
        """, (season["route_number"],))
        route_id = cursor.fetchone()
        if not route_id:
            continue
        route_id = route_id[0]

        cursor.execute("""
            INSERT INTO bus_trip_season
            (bus_trip_route_id, bus_trip_season_start_date, bus_trip_season_end_date)
            VALUES (?, ?, ?)
        """, (route_id, season["season_start_date"], season["season_end_date"]))

    # --- Flight seasons ---
    for season in flight_seasons:
        cursor.execute("""
            SELECT flight_route_id
            FROM flight_route
            WHERE route_number = ?
        """, (season["route_number"],))
        route_id = cursor.fetchone()
        if not route_id:
            continue
        route_id = route_id[0]

        cursor.execute("""
            INSERT INTO flight_season
            (flight_route_id, flight_season_start_date, flight_season_end_date)
            VALUES (?, ?, ?)
        """, (route_id, season["season_start_date"], season["season_end_date"]))

    conn.commit()

print(f"✅ Внесено {len(bus_trip_seasons)} bus trip seasons та {len(flight_seasons)} flight seasons")
