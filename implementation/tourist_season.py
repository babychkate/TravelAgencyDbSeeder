import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "tourist_seasons.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка туристичних сезонів ---
tourist_seasons = data.get("tourist seasons", [])

with conn.cursor() as cursor:
    count = 0
    for season in tourist_seasons:
        # отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            season["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            continue
        hotel_id = hotel_row[0]

        # отримуємо additional_info_id
        cursor.execute(
            "SELECT additional_info_id FROM additional_info WHERE additional_info_name = ?",
            season["additional_info_name"]
        )
        info_row = cursor.fetchone()
        if not info_row:
            continue
        additional_info_id = info_row[0]

        # вставка в tourist_season
        cursor.execute(
            """
            INSERT INTO tourist_season
            (hotel_id, additional_info_id, tourist_season_start_date, tourist_season_end_date)
            VALUES (?, ?, ?, ?)
            """,
            hotel_id,
            additional_info_id,
            season["tourist_season_start_date"],
            season["tourist_season_end_date"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} туристичних сезонів")
