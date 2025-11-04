import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "geography.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Додати країни ---
def insert_countries(countries):
    with conn.cursor() as cursor:
        for c in countries:
            cursor.execute(
                "INSERT INTO country (country_name) VALUES (?)",
                (c["country_name"],)
            )
        conn.commit()
    print(f"✅ Внесено {len(countries)} країн")

# --- Додати міста ---
def insert_cities(cities):
    with conn.cursor() as cursor:
        for city in cities:
            # Отримати country_id
            cursor.execute(
                "SELECT country_id FROM country WHERE country_name = ?",
                (city["country_name"],)
            )
            country_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO city (country_id, city_name) VALUES (?, ?)",
                (country_id, city["city_name"])
            )
        conn.commit()
    print(f"✅ Внесено {len(cities)} міст")

# --- Додати курорти ---
def insert_resorts(resorts):
    with conn.cursor() as cursor:
        for r in resorts:
            # Отримати country_id
            cursor.execute(
                "SELECT country_id FROM country WHERE country_name = ?",
                (r["country_name"],)
            )
            country_id = cursor.fetchone()[0]

            # Отримати vacation_type_id
            cursor.execute(
                "SELECT vacation_type_id FROM vacation_type WHERE vacation_type_name = ?",
                (r["vacation_type_name"],)
            )
            vacation_type_id = cursor.fetchone()[0]

            # Отримати city_id
            cursor.execute(
                "SELECT city_id FROM city WHERE city_name = ? AND country_id = ?",
                (r["city_name"], country_id)
            )
            city_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO resort (country_id, vacation_type_id, resort_name, resort_city_tax) VALUES (?, ?, ?, ?)",
                (country_id, vacation_type_id, r["resort_name"], r["resort_city_tax"])
            )
        conn.commit()
    print(f"✅ Внесено {len(resorts)} курортів")

# --- Додати аеропорти ---
def insert_airports(airports):
    with conn.cursor() as cursor:
        for a in airports:
            # city_id
            cursor.execute(
                "SELECT city_id FROM city WHERE city_name = ?",
                (a["city_name"],)
            )
            city_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO airport (airport_name, airport_code, airport_city_id) VALUES (?, ?, ?)",
                (a["airport_name"], a["airport_code"], city_id)
            )
        conn.commit()
    print(f"✅ Внесено {len(airports)} аеропортів")

# --- Додати автостанції ---
def insert_bus_stations(bus_stations):
    with conn.cursor() as cursor:
        for b in bus_stations:
            cursor.execute(
                "SELECT city_id FROM city WHERE city_name = ?",
                (b["city_name"],)
            )
            city_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO bus_station (bus_station_name, bus_station_city_id) VALUES (?, ?)",
                (b["bus_station_name"], city_id)
            )
        conn.commit()
    print(f"✅ Внесено {len(bus_stations)} автостанцій")

# --- Виклик функцій ---
insert_countries(data["countries"])
insert_cities(data["cities"])
insert_resorts(data["resorts"])
insert_airports(data["airports"])
insert_bus_stations(data["bus stations"])
