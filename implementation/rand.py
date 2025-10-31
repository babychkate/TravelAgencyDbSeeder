import json
from pathlib import Path
from sql_connection import conn  # твоє підключення

# --- Шлях до classifiers.json ---
file_path = Path(__file__).parent.parent / "data" / "geography.json"

# --- Зчитування JSON ---
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Функція пошуку ID за природним ключем ---
def get_id_by_natural_key(cursor, table, key_field, key_value):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {key_field} = ?", key_value)
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise ValueError(f"❌ Не знайдено '{key_value}' у таблиці '{table}'")

# --- 1. Внесення країн ---
countries = data.get("countries", [])
with conn.cursor() as cursor:
    for country in countries:
        cursor.execute(
            "INSERT INTO country (country_name) VALUES (?)",
            country["country_name"]
        )
    conn.commit()
print(f"✅ Внесено {len(countries)} записів у таблицю country")

# --- 2. Внесення міст (з пошуком country_id за country_name) ---
cities = data.get("cities", [])
with conn.cursor() as cursor:
    for city in cities:
        country_id = get_id_by_natural_key(cursor, "country", "country_name", city["country_name"])
        cursor.execute(
            "INSERT INTO city (city_name, country_id) VALUES (?, ?)",
            (city["city_name"], country_id)
        )
    conn.commit()
print(f"✅ Внесено {len(cities)} записів у таблицю city")
