import json
from pathlib import Path
from sql_connection import conn

file_path = Path(__file__).parent.parent / "data" / "geography.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

airport_list = data.get("airports", [])
bus_station_list = data.get("bus stations", [])

airport_count = 0
bus_station_count = 0

with conn.cursor() as cursor:
    # --- Вставка аеропортів ---
    for airport in airport_list:
        cursor.execute(
            "SELECT city_id FROM city WHERE city_name = ?",
            airport["city_name"]
        )
        city_row = cursor.fetchone()
        if city_row:
            city_id = city_row[0]
            cursor.execute(
                "INSERT INTO airport (airport_name, airport_code, airport_city_id) VALUES (?, ?, ?)",
                airport["airport_name"], airport["airport_code"], city_id
            )
            airport_count += 1

    # --- Вставка автобусних станцій ---
    for station in bus_station_list:
        cursor.execute(
            "SELECT city_id FROM city WHERE city_name = ?",
            station["city_name"]
        )
        city_row = cursor.fetchone()
        if city_row:
            city_id = city_row[0]
            cursor.execute(
                "INSERT INTO bus_station (bus_station_name, bus_station_city_id) VALUES (?, ?)",
                station["bus_station_name"], city_id
            )
            bus_station_count += 1

    conn.commit()

print(f"✅ Внесено {airport_count} аеропортів")
print(f"✅ Внесено {bus_station_count} автобусних станцій")
