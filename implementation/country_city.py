import json
from pathlib import Path
from sql_connection import conn 

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "geography.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка країн ---
countries = data.get("countries", [])
with conn.cursor() as cursor:
    for country in countries:
        cursor.execute(
            "INSERT INTO country (country_name) VALUES (?)",
            country["country_name"]
        )
    conn.commit()
print(f"✅ Внесено {len(countries)} країн")

# --- Вставка міст з прив'язкою до country_id ---
cities = data.get("cities", [])
with conn.cursor() as cursor:
    for city in cities:
        # знаходимо id країни за country_name
        cursor.execute(
            "SELECT country_id FROM country WHERE country_name = ?",
            city["country_name"]
        )
        country_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO city (city_name, country_id) VALUES (?, ?)",
            city["city_name"], country_id
        )
    conn.commit()
print(f"✅ Внесено {len(cities)} міст")
