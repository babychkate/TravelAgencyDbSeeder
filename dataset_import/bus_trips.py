import json
from pathlib import Path
from datetime import datetime
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "bus_trip.json"

with open(file_path, "r", encoding="utf-8") as f:
    bus_trips = json.load(f).get("bus trips", [])

with conn.cursor() as cursor:
    for trip in bus_trips:
        # Отримуємо bus_trip_route_id
        cursor.execute("""
            SELECT bus_trip_route_id
            FROM bus_trip_route
            WHERE route_number = ?
        """, (trip["route_number"],))
        route_row = cursor.fetchone()
        if not route_row:
            continue
        route_id = route_row[0]

        # Конвертація дати та часу у datetime
        departure_dt = datetime.strptime(f"{trip['date']} {trip['bus_trip_departure_time']}", "%Y-%m-%d %H:%M")
        arrival_dt = datetime.strptime(f"{trip['date']} {trip['bus_trip_arrival_time']}", "%Y-%m-%d %H:%M")

        # Перевірка дубліката
        cursor.execute("""
            SELECT 1
            FROM bus_trip
            WHERE bus_trip_route_id = ? AND bus_trip_departure_datetime = ? AND bus_trip_arrival_datetime = ?
        """, (route_id, departure_dt, arrival_dt))
        if cursor.fetchone():
            continue

        # Вставка
        cursor.execute("""
            INSERT INTO bus_trip (bus_trip_route_id, bus_trip_expected_price, bus_trip_departure_datetime, bus_trip_arrival_datetime)
            VALUES (?, ?, ?, ?)
        """, (route_id, trip["bus_trip_expected_price"], departure_dt, arrival_dt))

    conn.commit()

print(f"✅ Внесено {len(bus_trips)} bus trips")
