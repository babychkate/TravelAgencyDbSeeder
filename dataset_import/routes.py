import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "routes.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

bus_trip_routes = data.get("bus trip routes", [])
flight_routes = data.get("flight routes", [])

# --- Bus trip routes ---
with conn.cursor() as cursor:
    for trip in bus_trip_routes:
        # Отримуємо id типу маршруту
        cursor.execute(
            "SELECT bus_trip_route_type_id FROM bus_trip_route_type WHERE bus_trip_route_type_name = ?",
            (trip["bus_trip_route_type_name"],)
        )
        route_type_id_row = cursor.fetchone()
        if not route_type_id_row: continue
        route_type_id = route_type_id_row[0]

        # --- Departure station ---
        cursor.execute("SELECT city_id FROM city WHERE city_name = ?", (trip["departure_city_name"],))
        departure_city_row = cursor.fetchone()
        if not departure_city_row: continue
        departure_city_id = departure_city_row[0]

        cursor.execute(
            "SELECT bus_station_id FROM bus_station WHERE bus_station_city_id = ?",
            (departure_city_id,)
        )
        departure_station_row = cursor.fetchone()
        if not departure_station_row: continue
        departure_station_id = departure_station_row[0]

        # --- Arrival station ---
        cursor.execute("SELECT city_id FROM city WHERE city_name = ?", (trip["arrival_city_name"],))
        arrival_city_row = cursor.fetchone()
        if not arrival_city_row: continue
        arrival_city_id = arrival_city_row[0]

        cursor.execute(
            "SELECT bus_station_id FROM bus_station WHERE bus_station_city_id = ?",
            (arrival_city_id,)
        )
        arrival_station_row = cursor.fetchone()
        if not arrival_station_row: continue
        arrival_station_id = arrival_station_row[0]

        # --- Bus company ---
        cursor.execute(
            "SELECT bus_company_id FROM bus_company WHERE bus_company_name = ?",
            (trip["bus_company_name"]["bus_company_name"],)
        )
        company_row = cursor.fetchone()
        if not company_row: continue
        company_id = company_row[0]

        # --- Вставка в таблицю ---
        cursor.execute("""
            INSERT INTO bus_trip_route
            (bus_trip_route_type_id, departure_bus_station_id, arrival_bus_station_id, bus_company_id, route_number, bus_trip_duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (route_type_id, departure_station_id, arrival_station_id, company_id, trip["route_number"], trip["bus_trip_duration"]))

    conn.commit()
print(f"✅ Внесено {len(bus_trip_routes)} bus trip routes")

# --- Flight routes ---
with conn.cursor() as cursor:
    for trip in flight_routes:
        # Отримуємо id типу маршруту
        cursor.execute(
            "SELECT flight_route_type_id FROM flight_route_type WHERE flight_route_type_name = ?",
            (trip["flight_route_type_name"],)
        )
        route_type_row = cursor.fetchone()
        if not route_type_row: continue
        route_type_id = route_type_row[0]

        # --- Departure airport ---
        cursor.execute("SELECT city_id FROM city WHERE city_name = ?", (trip["departure_city_name"],))
        departure_city_row = cursor.fetchone()
        if not departure_city_row: continue
        departure_city_id = departure_city_row[0]

        cursor.execute("SELECT airport_id FROM airport WHERE airport_city_id = ?", (departure_city_id,))
        departure_airport_row = cursor.fetchone()
        if not departure_airport_row: continue
        departure_airport_id = departure_airport_row[0]

        # --- Arrival airport ---
        cursor.execute("SELECT city_id FROM city WHERE city_name = ?", (trip["arrival_city_name"],))
        arrival_city_row = cursor.fetchone()
        if not arrival_city_row: continue
        arrival_city_id = arrival_city_row[0]

        cursor.execute("SELECT airport_id FROM airport WHERE airport_city_id = ?", (arrival_city_id,))
        arrival_airport_row = cursor.fetchone()
        if not arrival_airport_row: continue
        arrival_airport_id = arrival_airport_row[0]

        # --- Airline ---
        cursor.execute(
            "SELECT airline_id FROM airline WHERE airline_name = ?",
            (trip["airline_name"]["airline_name"],)
        )
        airline_row = cursor.fetchone()
        if not airline_row: continue
        airline_id = airline_row[0]

        # --- Вставка ---
        cursor.execute("""
            INSERT INTO flight_route
            (flight_route_type_id, departure_airport_id, arrival_airport_id, airline_id, route_number, flight_duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            route_type_id,
            departure_airport_id,
            arrival_airport_id,
            airline_id,
            trip["route_number"],
            trip["flight_duration"]
        ))

    conn.commit()
print(f"✅ Внесено {len(flight_routes)} flight routes")

