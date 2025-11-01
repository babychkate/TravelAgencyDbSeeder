import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "room_price_season.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

room_price_seasons = data.get("room price seasons", [])

with conn.cursor() as cursor:
    added_count = 0
    for rps in room_price_seasons:
        # Отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            rps["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            continue
        hotel_id = hotel_row[0]

        # Отримуємо tourist_season_id
        cursor.execute(
            """
            SELECT ts.tourist_season_id
            FROM tourist_season ts
            WHERE ts.tourist_season_start_date = ?
              AND ts.tourist_season_end_date = ?
              AND ts.hotel_id = ?
            """,
            rps["tourist_season_start_date"],
            rps["tourist_season_end_date"],
            hotel_id
        )
        season_row = cursor.fetchone()
        if not season_row:
            continue
        tourist_season_id = season_row[0]

        # Отримуємо hotel_room_type_id
        cursor.execute(
            """
            SELECT hrt.hotel_room_type_id
            FROM hotel_room_type hrt
            JOIN room_type rt ON hrt.room_type_id = rt.room_type_id
            WHERE rt.room_type_name = ?
              AND hrt.hotel_room_type_max_adults = ?
              AND hrt.hotel_room_type_max_children = ?
            """,
            rps["hotel_room_type_name"],
            rps["max_adults"],
            rps["max_children"]
        )
        room_type_row = cursor.fetchone()
        if not room_type_row:
            continue
        hotel_room_type_id = room_type_row[0]

        # Вставка в room_price_season
        cursor.execute(
            """
            INSERT INTO room_price_season
            (hotel_room_type_id, tourist_season_id, room_price_per_person)
            VALUES (?, ?, ?)
            """,
            hotel_room_type_id, tourist_season_id, rps["room_price_per_person"]
        )
        added_count += 1

    conn.commit()

print(f"✅ Внесено {added_count} записів у room_price_season")
