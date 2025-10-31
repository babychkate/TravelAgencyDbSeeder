import json
from pathlib import Path
from sql_connection import conn

file_path = Path(__file__).parent.parent / "data" / "hotel_base.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

facility_list = data.get("facilities", [])

with conn.cursor() as cursor:
    added_count = 0
    for facility in facility_list:
        # Отримуємо category_id для FK
        cursor.execute(
            "SELECT category_of_facility_id FROM category_of_facility WHERE category_of_facility_name = ?",
            facility["category_of_facility_name"]
        )
        category_row = cursor.fetchone()
        if category_row:
            category_id = category_row[0]
            cursor.execute(
                "INSERT INTO facility (facility_name, category_of_facility_id) VALUES (?, ?)",
                facility["facility_name"], category_id
            )
            added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} facilities")
