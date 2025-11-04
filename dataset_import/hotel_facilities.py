import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotel_facilities.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_hotel_facilities(hotel_facilities):
    with conn.cursor() as cursor:
        added_count = 0
        for hf in hotel_facilities:
            # Отримати hotel_id
            cursor.execute("SELECT hotel_id FROM hotel WHERE hotel_name = ?", (hf["hotel_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Готель '{hf['hotel_name']}' не знайдено — пропускаємо")
                continue
            hotel_id = row[0]

            # Отримати facility_id
            cursor.execute("SELECT facility_id FROM facility WHERE facility_name = ?", (hf["facility_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Facility '{hf['facility_name']}' не знайдено — пропускаємо")
                continue
            facility_id = row[0]

            # Вставка у hotel_facility
            cursor.execute(
                "INSERT INTO hotel_facility (hotel_id, facility_id, hotel_facility_is_paid) VALUES (?, ?, ?)",
                (hotel_id, facility_id, hf["hotel_facility_is_paid"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} hotel facilities")

# --- Виклик ---
insert_hotel_facilities(data.get("hotel facilities", []))
