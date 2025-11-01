import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "hotels.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

hotels = data.get("hotels", [])

with conn.cursor() as cursor:
    added_count = 0
    for hotel in hotels:
        # отримуємо city_id
        cursor.execute(
            "SELECT city_id FROM city WHERE city_name = ?",
            hotel["city_name"]
        )
        city_row = cursor.fetchone()
        if not city_row:
            continue
        city_id = city_row[0]

        # отримуємо resort_id
        cursor.execute(
            "SELECT resort_id FROM resort WHERE resort_name = ?",
            hotel["resort_name"]
        )
        resort_row = cursor.fetchone()
        if not resort_row:
            continue
        resort_id = resort_row[0]

        # вставка у таблицю hotel
        cursor.execute(
            """
            INSERT INTO hotel
            (resort_id, city_id, hotel_name, hotel_description, hotel_room_count, hotel_rate, 
             hotel_latitude, hotel_longitude, hotel_email, hotel_phone, hotel_website, hotel_area, hotel_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            resort_id,
            city_id,
            hotel["hotel_name"],
            hotel["hotel_description"],
            hotel["hotel_room_count"],
            hotel["hotel_rate"],
            hotel["hotel_latitude"],
            hotel["hotel_longitude"],
            hotel["hotel_email"],
            hotel["hotel_phone"],
            hotel["hotel_website"],
            hotel["hotel_area"],
            hotel["hotel_address"]
        )
        added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} готелів")
