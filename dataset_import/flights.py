import json
from pathlib import Path
from datetime import datetime
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "flight.json"

with open(file_path, "r", encoding="utf-8") as f:
    flights = json.load(f).get("flights", [])

with conn.cursor() as cursor:
    for flight in flights:
        # Отримуємо flight_route_id
        cursor.execute("""
            SELECT flight_route_id
            FROM flight_route
            WHERE route_number = ?
        """, (flight["route_number"],))
        route_row = cursor.fetchone()
        if not route_row:
            continue
        route_id = route_row[0]

        # Конвертація дати та часу у datetime
        departure_dt = datetime.strptime(f"{flight['date']} {flight['flight_trip_departure_time']}", "%Y-%m-%d %H:%M")
        arrival_dt = datetime.strptime(f"{flight['date']} {flight['flight_trip_arrival_time']}", "%Y-%m-%d %H:%M")

        # Перевірка дубліката
        cursor.execute("""
            SELECT 1
            FROM flight
            WHERE flight_route_id = ? AND flight_departure_datetime = ? AND flight_arrival_datetime = ?
        """, (route_id, departure_dt, arrival_dt))
        if cursor.fetchone():
            continue

        # Вставка
        cursor.execute("""
            INSERT INTO flight (flight_route_id, flight_expected_price, flight_departure_datetime, flight_arrival_datetime)
            VALUES (?, ?, ?, ?)
        """, (route_id, flight["flight_trip_expected_price"], departure_dt, arrival_dt))

    conn.commit()

print(f"✅ Внесено {len(flights)} flights")
