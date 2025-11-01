import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "tour_accommodation.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

tour_accommodations = data.get("tour accommodations", [])

with conn.cursor() as cursor:
    added_count = 0

    for ta in tour_accommodations:
        # --- Отримуємо hotel_id ---
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            ta["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            print(f"⚠️ Пропущено: не знайдено готель {ta['hotel_name']}")
            continue
        hotel_id = hotel_row[0]

        # --- Отримуємо tourist_season_id ---
        cursor.execute(
            """
            SELECT tourist_season_id
            FROM tourist_season
            WHERE tourist_season_start_date = ?
              AND tourist_season_end_date = ?
              AND hotel_id = ?
            """,
            ta["tourist_season_start_date"],
            ta["tourist_season_end_date"],
            hotel_id
        )
        season_row = cursor.fetchone()
        if not season_row:
            print(f"⚠️ Пропущено: не знайдено сезон для {ta['hotel_name']}")
            continue
        tourist_season_id = season_row[0]

        # --- Отримуємо room_price_season_id ---
        cursor.execute(
            """
            SELECT rps.room_price_season_id
            FROM room_price_season rps
            JOIN hotel_room_type hrt
              ON rps.hotel_room_type_id = hrt.hotel_room_type_id
            JOIN room_type rt
              ON hrt.room_type_id = rt.room_type_id
            WHERE rps.tourist_season_id = ?
              AND rt.room_type_name = ?
              AND hrt.hotel_room_type_max_adults = ?
              AND hrt.hotel_room_type_max_children = ?
            """,
            tourist_season_id,
            ta["hotel_room_type_name"],
            ta["max_adults"],
            ta["max_children"]
        )
        room_row = cursor.fetchone()
        if not room_row:
            print(f"⚠️ Пропущено: не знайдено room_price_season для {ta['hotel_room_type_name']}")
            continue
        room_price_season_id = room_row[0]

        # --- Отримуємо meal_price_season_id ---
        cursor.execute(
            """
            SELECT mps.meal_price_season_id
            FROM meal_price_season mps
            JOIN meal_type mt
              ON mps.meal_type_id = mt.meal_type_id
            WHERE mps.tourist_season_id = ?
              AND mt.meal_type_name = ?
            """,
            tourist_season_id,
            ta["meal_type_name"]
        )
        meal_row = cursor.fetchone()
        if not meal_row:
            print(f"⚠️ Пропущено: не знайдено meal_price_season для {ta['meal_type_name']}")
            continue
        meal_price_season_id = meal_row[0]

        # --- Додаємо запис у tour_accommodation ---
        cursor.execute(
            """
            INSERT INTO tour_accommodation
            (room_price_season_id, meal_price_season_id, tour_accommodation_start_date, tour_accommodation_end_date)
            VALUES (?, ?, ?, ?)
            """,
            room_price_season_id,
            meal_price_season_id,
            ta["tourist_season_start_date"],
            ta["tourist_season_end_date"]
        )
        added_count += 1

    conn.commit()

print(f"✅ Внесено {added_count} записів у tour_accommodation")
