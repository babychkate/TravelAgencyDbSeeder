import json
from pathlib import Path
from sql_connection import conn

file_path = Path(__file__).parent.parent / "data" / "hotel_base.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

nearby_list = data.get("nearby objects", [])

with conn.cursor() as cursor:
    added_count = 0
    for obj in nearby_list:
        # Отримуємо nearby_object_type_id
        cursor.execute(
            "SELECT nearby_object_type_id FROM nearby_object_type WHERE nearby_object_type_name = ?",
            obj["nearby_object_type_name"]
        )
        type_row = cursor.fetchone()
        if not type_row:
            continue
        type_id = type_row[0]

        cursor.execute(
            "INSERT INTO nearby_object (nearby_object_type_id, nearby_object_name, nearby_object_address) VALUES (?, ?, ?)",
            type_id, obj["nearby_object_name"], obj["nearby_object_address"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} nearby objects")
