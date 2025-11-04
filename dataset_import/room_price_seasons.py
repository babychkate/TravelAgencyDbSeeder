import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "room_price_seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_room_price_seasons(price_seasons):
    with conn.cursor() as cursor:
        added_count = 0
        for p in price_seasons:
            # Отримати hotel_room_type_id
            cursor.execute(
                """
                SELECT hrt.hotel_room_type_id
                FROM hotel_room_type hrt
                JOIN room_type rt ON hrt.room_type_id = rt.room_type_id
                WHERE rt.room_type_name = ? 
                  AND hrt.hotel_room_type_max_adults = ?
                  AND hrt.hotel_room_type_max_children = ?
                """,
                (p["hotel_room_type_name"], p["max_adults"], p["max_children"])
            )
            room_type_row = cursor.fetchone()
            if not room_type_row:
                print(f"⚠ Hotel room type '{p['hotel_room_type_name']}' не знайдено — пропускаємо")
                continue
            hotel_room_type_id = room_type_row[0]

            # Отримати tourist_season_id
            cursor.execute(
                """
                SELECT ts.tourist_season_id
                FROM tourist_season ts
                JOIN hotel h ON ts.hotel_id = h.hotel_id
                WHERE h.hotel_name = ? 
                  AND ts.tourist_season_start_date = ?
                  AND ts.tourist_season_end_date = ?
                """,
                (p["hotel_name"], p["tourist_season_start_date"], p["tourist_season_end_date"])
            )
            season_row = cursor.fetchone()
            if not season_row:
                print(f"⚠ Tourist season for '{p['hotel_name']}' з датами {p['tourist_season_start_date']} - {p['tourist_season_end_date']} не знайдено — пропускаємо")
                continue
            tourist_season_id = season_row[0]

            # Вставка ціни
            cursor.execute(
                """
                INSERT INTO room_price_season (hotel_room_type_id, tourist_season_id, room_price_per_person)
                VALUES (?, ?, ?)
                """,
                (hotel_room_type_id, tourist_season_id, p["room_price_per_person"])
            )
            added_count += 1

        conn.commit()
    print(f"✅ Внесено {added_count} room price seasons")

# --- Виклик ---
insert_room_price_seasons(data.get("room price seasons", []))
