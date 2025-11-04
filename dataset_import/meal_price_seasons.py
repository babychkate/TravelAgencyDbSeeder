import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "meal_price_seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_meal_price_seasons(meal_price_seasons):
    with conn.cursor() as cursor:
        added_count = 0
        for m in meal_price_seasons:
            # Отримати meal_type_id
            cursor.execute(
                "SELECT meal_type_id FROM meal_type WHERE meal_type_name = ?",
                (m["meal_type_name"],)
            )
            meal_row = cursor.fetchone()
            if not meal_row:
                print(f"⚠ Meal type '{m['meal_type_name']}' не знайдено — пропускаємо")
                continue
            meal_type_id = meal_row[0]

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
                (m["hotel_name"], m["tourist_season_start_date"], m["tourist_season_end_date"])
            )
            season_row = cursor.fetchone()
            if not season_row:
                print(f"⚠ Tourist season для '{m['hotel_name']}' з датами {m['tourist_season_start_date']} - {m['tourist_season_end_date']} не знайдено — пропускаємо")
                continue
            tourist_season_id = season_row[0]

            # Вставка ціни
            cursor.execute(
                """
                INSERT INTO meal_price_season (meal_type_id, tourist_season_id, meal_price_per_person)
                VALUES (?, ?, ?)
                """,
                (meal_type_id, tourist_season_id, m["meal_price_per_person"])
            )
            added_count += 1

        conn.commit()
    print(f"✅ Внесено {added_count} meal price seasons")

# --- Виклик ---
insert_meal_price_seasons(data.get("meal price seasons", []))
