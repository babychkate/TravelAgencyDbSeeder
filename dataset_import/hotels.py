import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotels.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка готелів ---
def insert_hotels(hotels):
    with conn.cursor() as cursor:
        added_count = 0
        for h in hotels:
            # Отримати city_id
            cursor.execute(
                "SELECT city_id FROM city WHERE city_name = ?",
                (h["city_name"],)
            )
            city_row = cursor.fetchone()
            if not city_row:
                print(f"⚠ Місто '{h['city_name']}' не знайдено — пропускаємо готель '{h['hotel_name']}'")
                continue
            city_id = city_row[0]

            # Отримати resort_id
            cursor.execute(
                "SELECT resort_id FROM resort WHERE resort_name = ?",
                (h["resort_name"],)
            )
            resort_row = cursor.fetchone()
            if not resort_row:
                print(f"⚠ Курорт '{h['resort_name']}' не знайдено — пропускаємо готель '{h['hotel_name']}'")
                continue
            resort_id = resort_row[0]

            # Вставка готелю
            cursor.execute(
                """
                INSERT INTO hotel (
                    resort_id, city_id, hotel_name, hotel_description, hotel_room_count, hotel_rate,
                    hotel_latitude, hotel_longitude, hotel_email, hotel_phone, hotel_website,
                    hotel_area, hotel_address
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    resort_id, city_id, h["hotel_name"], h["hotel_description"], h["hotel_room_count"],
                    h["hotel_rate"], h["hotel_latitude"], h["hotel_longitude"], h["hotel_email"],
                    h["hotel_phone"], h["hotel_website"], h["hotel_area"], h["hotel_address"]
                )
            )
            added_count += 1

        conn.commit()
    print(f"✅ Внесено {added_count} готелів")

# --- Виклик функції ---
insert_hotels(data.get("hotels", []))
