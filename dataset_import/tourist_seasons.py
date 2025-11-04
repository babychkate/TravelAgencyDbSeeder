import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "tourist_seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка туристичних сезонів ---
def insert_tourist_seasons(seasons):
    with conn.cursor() as cursor:
        added_count = 0
        for s in seasons:
            # Отримати hotel_id
            cursor.execute(
                "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
                (s["hotel_name"],)
            )
            hotel_row = cursor.fetchone()
            if not hotel_row:
                print(f"⚠ Hotel '{s['hotel_name']}' не знайдено — пропускаємо")
                continue
            hotel_id = hotel_row[0]

            # Отримати additional_info_id
            cursor.execute(
                "SELECT additional_info_id FROM additional_info WHERE additional_info_name = ?",
                (s["additional_info_name"],)
            )
            info_row = cursor.fetchone()
            if not info_row:
                print(f"⚠ Additional info '{s['additional_info_name']}' не знайдено — пропускаємо")
                continue
            additional_info_id = info_row[0]

            # Вставка туристичного сезону
            cursor.execute(
                """
                INSERT INTO tourist_season (hotel_id, additional_info_id, tourist_season_start_date, tourist_season_end_date)
                VALUES (?, ?, ?, ?)
                """,
                (hotel_id, additional_info_id, s["tourist_season_start_date"], s["tourist_season_end_date"])
            )
            added_count += 1

        conn.commit()
    print(f"✅ Внесено {added_count} tourist seasons")

# --- Виклик ---
insert_tourist_seasons(data.get("tourist seasons", []))
