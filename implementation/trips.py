import json
from pathlib import Path
from datetime import datetime
from sql_connection import conn

file_path = Path(__file__).parent.parent / "data" / "trips.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

bus_trips_data = data.get("bus trips", [])
flights_data = data.get("flights", [])

with conn.cursor() as cursor:
    added_bus = 0
    added_flight = 0

    # --- BUS TRIPS ---
    for bt in bus_trips_data:
        # Знаходимо bus_trip_route_id
        cursor.execute(
            "SELECT bus_trip_route_id FROM bus_trip_route WHERE route_number = ?",
            bt["route_number"]
        )
        route_row = cursor.fetchone()
        if not route_row:
            print(f"⚠️ Пропущено: не знайдено bus_trip_route для {bt['route_number']}")
            continue
        bus_trip_route_id = route_row[0]

        # Формуємо datetime для departure та arrival
        departure_dt = datetime.strptime(f"{bt['date']} {bt['bus_trip_departure_time']}", "%Y-%m-%d %H:%M")
        arrival_dt = datetime.strptime(f"{bt['date']} {bt['bus_trip_arrival_time']}", "%Y-%m-%d %H:%M")

        # Вставка в таблицю bus_trip
        cursor.execute(
            """
            INSERT INTO bus_trip
            (bus_trip_route_id, bus_trip_expected_price, bus_trip_departure_datetime, bus_trip_arrival_datetime)
            VALUES (?, ?, ?, ?)
            """,
            bus_trip_route_id,
            bt["bus_trip_expected_price"],
            departure_dt,
            arrival_dt
        )
        added_bus += 1

    # --- FLIGHTS ---
    for fl in flights_data:
        # Знаходимо flight_route_id
        cursor.execute(
            "SELECT flight_route_id FROM flight_route WHERE route_number = ?",
            fl["route_number"]
        )
        route_row = cursor.fetchone()
        if not route_row:
            print(f"⚠️ Пропущено: не знайдено flight_route для {fl['route_number']}")
            continue
        flight_route_id = route_row[0]

        # Формуємо datetime для departure та arrival
        departure_dt = datetime.strptime(f"{fl['date']} {fl['flight_trip_departure_time']}", "%Y-%m-%d %H:%M")
        arrival_dt = datetime.strptime(f"{fl['date']} {fl['flight_trip_arrival_time']}", "%Y-%m-%d %H:%M")

        # Вставка в таблицю flight
        cursor.execute(
            """
            INSERT INTO flight
            (flight_route_id, flight_expected_price, flight_departure_datetime, flight_arrival_datetime)
            VALUES (?, ?, ?, ?)
            """,
            flight_route_id,
            fl["flight_trip_expected_price"],
            departure_dt,
            arrival_dt
        )
        added_flight += 1

    conn.commit()

print(f"✅ Внесено {added_bus} записів у bus_trip")
print(f"✅ Внесено {added_flight} записів у flight")
