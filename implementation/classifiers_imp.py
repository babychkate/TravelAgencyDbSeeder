import json
from pathlib import Path
from sql_connection import conn 

# --- Шлях до файлу classifiers.json ---
file_path = Path(__file__).parent.parent / "data" / "classifiers.json"

# --- Зчитування JSON ---
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Функція для вставки простих класифікаторів ---
def insert_simple(table_name, field_name, records):
    with conn.cursor() as cursor:
        for record in records:
            cursor.execute(
                f"INSERT INTO {table_name} ({field_name}) VALUES (?)",
                record[field_name]
            )
        conn.commit()
    print(f"✅ Внесено {len(records)} записів у таблицю {table_name}")

simple_classifiers = [
    ("additional_info", "additional_info_name", "additional infos"),
    ("bed_type", "bed_type_name", "bed types"),
    ("booking_status", "booking_status_name", "booking statuses"),
    ("bus_trip_route_type", "bus_trip_route_type_name", "bus trip route types"),
    ("category_of_facility", "category_of_facility_name", "category of facilities"),
    ("flight_route_type", "flight_route_type_name", "flight route types"),
    ("room_type", "room_type_name", "room types"),
    ("meal_type", "meal_type_name", "meal types"),
    ("nearby_object_type", "nearby_object_type_name", "nearby object types"),
    ("package_tour_status", "package_tour_status_name", "package tour statuses"),
    ("policy_type", "policy_type_name", "policy types"),
    ("vacation_type", "vacation_type_name", "vacation types")
]

# --- Вставка всіх простих класифікаторів ---
for table, field, json_key in simple_classifiers:
    records = data.get(json_key, [])
    if records:
        insert_simple(table, field, records)
