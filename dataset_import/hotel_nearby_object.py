import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotel_nearby_objects.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_nearby_object_locations(locations):
    with conn.cursor() as cursor:
        added_count = 0
        for loc in locations:
            # Отримати hotel_id
            cursor.execute("SELECT hotel_id FROM hotel WHERE hotel_name = ?", (loc["hotel_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Готель '{loc['hotel_name']}' не знайдено — пропускаємо")
                continue
            hotel_id = row[0]

            # Отримати nearby_object_id
            cursor.execute("SELECT nearby_object_id FROM nearby_object WHERE nearby_object_name = ?", (loc["nearby_object_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Nearby object '{loc['nearby_object_name']}' не знайдено — пропускаємо")
                continue
            nearby_object_id = row[0]

            # Вставка у nearby_object_location
            cursor.execute(
                "INSERT INTO nearby_object_location (hotel_id, nearby_object_id, from_hotel_to_object_distance_km, time_to_object_by_transport_min, time_to_object_by_walk_min) VALUES (?, ?, ?, ?, ?)",
                (
                    hotel_id,
                    nearby_object_id,
                    loc.get("from_hotel_to_object_distance_km"),
                    loc.get("time_to_object_by_transport_min"),
                    loc.get("time_to_object_by_walk_min")
                )
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} nearby object locations")

# --- Виклик ---
insert_nearby_object_locations(data.get("hotel nearby objects", []))
