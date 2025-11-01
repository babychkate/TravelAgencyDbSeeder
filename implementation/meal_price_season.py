import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "meal_price_season.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

meal_price_seasons = data.get("meal price seasons", [])

with conn.cursor() as cursor:
    added_count = 0
    for mps in meal_price_seasons:
        # Отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            mps["hotel_name"]
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
            mps["tourist_season_start_date"],
            mps["tourist_season_end_date"],
            hotel_id
        )
        season_row = cursor.fetchone()
        if not season_row:
            continue
        tourist_season_id = season_row[0]

        # Отримуємо meal_type_id
        cursor.execute(
            "SELECT meal_type_id FROM meal_type WHERE meal_type_name = ?",
            mps["meal_type_name"]
        )
        meal_type_row = cursor.fetchone()
        if not meal_type_row:
            continue
        meal_type_id = meal_type_row[0]

        # Вставка в meal_price_season
        cursor.execute(
            """
            INSERT INTO meal_price_season
            (meal_type_id, tourist_season_id, meal_price_per_person)
            VALUES (?, ?, ?)
            """,
            meal_type_id, tourist_season_id, mps["meal_price_per_person"]
        )
        added_count += 1

    conn.commit()

print(f"✅ Внесено {added_count} записів у meal_price_season")
