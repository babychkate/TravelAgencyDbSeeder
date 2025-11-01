import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "routes.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Bus Trip Routes ---
bus_routes = data.get("bus trip routes", [])

with conn.cursor() as cursor:
    added_count = 0
    for route in bus_routes:
        # Отримуємо bus_trip_route_type_id
        cursor.execute(
            "SELECT bus_trip_route_type_id FROM bus_trip_route_type WHERE bus_trip_route_type_name = ?",
            route["bus_trip_route_type_name"]
        )
        type_row = cursor.fetchone()
        if not type_row:
            continue
        bus_trip_route_type_id = type_row[0]

        # Отримуємо departure_bus_station_id
        cursor.execute(
            "SELECT bus_station_id FROM bus_station WHERE bus_station_name = ?",
            route["departure_bus_station_name"]
        )
        dep_row = cursor.fetchone()
        if not dep_row:
            continue
        departure_bus_station_id = dep_row[0]

        # Отримуємо arrival_bus_station_id
        cursor.execute(
            "SELECT bus_station_id FROM bus_station WHERE bus_station_name = ?",
            route["arrival_bus_station_name"]
        )
        arr_row = cursor.fetchone()
        if not arr_row:
            continue
        arrival_bus_station_id = arr_row[0]

        # Отримуємо bus_company_id
        cursor.execute(
            "SELECT bus_company_id FROM bus_company WHERE bus_company_name = ?",
            route["bus_company_name"]
        )
        company_row = cursor.fetchone()
        if not company_row:
            continue
        bus_company_id = company_row[0]

        # Вставка в bus_trip_route
        cursor.execute(
            """
            INSERT INTO bus_trip_route
            (bus_trip_route_type_id, departure_bus_station_id, arrival_bus_station_id, bus_company_id, route_number, bus_trip_duration)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            bus_trip_route_type_id,
            departure_bus_station_id,
            arrival_bus_station_id,
            bus_company_id,
            route["route_number"],
            route["bus_trip_duration"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} bus_trip_routes")

# --- 2. Flight Routes ---
flight_routes = data.get("flight routes", [])

with conn.cursor() as cursor:
    added_count = 0
    for route in flight_routes:
        # Отримуємо flight_route_type_id
        cursor.execute(
            "SELECT flight_route_type_id FROM flight_route_type WHERE flight_route_type_name = ?",
            route["flight_route_type_name"]
        )
        type_row = cursor.fetchone()
        if not type_row:
            continue
        flight_route_type_id = type_row[0]

        # Отримуємо departure_airport_id
        cursor.execute(
            "SELECT airport_id FROM airport WHERE airport_name = ?",
            route["departure_airport_name"]
        )
        dep_row = cursor.fetchone()
        if not dep_row:
            continue
        departure_airport_id = dep_row[0]

        # Отримуємо arrival_airport_id
        cursor.execute(
            "SELECT airport_id FROM airport WHERE airport_name = ?",
            route["arrival_airport_name"]
        )
        arr_row = cursor.fetchone()
        if not arr_row:
            continue
        arrival_airport_id = arr_row[0]

        # Отримуємо airline_id
        cursor.execute(
            "SELECT airline_id FROM airline WHERE airline_name = ?",
            route["airline_name"]
        )
        airline_row = cursor.fetchone()
        if not airline_row:
            continue
        airline_id = airline_row[0]

        # Вставка в flight_route
        cursor.execute(
            """
            INSERT INTO flight_route
            (flight_route_type_id, departure_airport_id, arrival_airport_id, airline_id, route_number, flight_duration)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            flight_route_type_id,
            departure_airport_id,
            arrival_airport_id,
            airline_id,
            route["flight_number"],
            route["flight_duration"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} flight_routes")
