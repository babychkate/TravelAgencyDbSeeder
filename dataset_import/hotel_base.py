import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotel_base.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка зручностей (facilities) ---
def insert_facilities(facilities):
    with conn.cursor() as cursor:
        for f in facilities:
            # Отримати category_of_facility_id
            cursor.execute(
                "SELECT category_of_facility_id FROM category_of_facility WHERE category_of_facility_name = ?",
                (f["category_of_facility_name"],)
            )
            category_id = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO facility (category_of_facility_id, facility_name) VALUES (?, ?)",
                (category_id, f["facility_name"])
            )
        conn.commit()
    print(f"✅ Внесено {len(facilities)} зручностей")

# --- Вставка nearby objects ---
def insert_nearby_objects(nearby_objects):
    with conn.cursor() as cursor:
        for obj in nearby_objects:
            # Отримати nearby_object_type_id
            cursor.execute(
                "SELECT nearby_object_type_id FROM nearby_object_type WHERE nearby_object_type_name = ?",
                (obj["nearby_object_type_name"],)
            )
            type_id = cursor.fetchone()[0]
            
            cursor.execute(
                "INSERT INTO nearby_object (nearby_object_type_id, nearby_object_name, nearby_object_address) VALUES (?, ?, ?)",
                (type_id, obj["nearby_object_name"], obj["nearby_object_address"])
            )
        conn.commit()
    print(f"✅ Внесено {len(nearby_objects)} nearby objects")

# --- Виклик функцій ---
insert_facilities(data["facilities"])
insert_nearby_objects(data["nearby objects"])
