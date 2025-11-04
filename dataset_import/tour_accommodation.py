import json
from pathlib import Path
from sql_connection import conn  # твій підключений pyodbc

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "tour_accommodations.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_tour_accommodations(tour_accommodations):
    with conn.cursor() as cursor:
        for t in tour_accommodations:
            # --- Отримати hotel_id ---
            cursor.execute(
                "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
                (t["hotel_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Hotel '{t['hotel_name']}' не знайдено — пропускаємо")
                continue
            hotel_id = row[0]

            # --- Отримати tourist_season_id ---
            cursor.execute(
                "SELECT tourist_season_id FROM tourist_season "
                "WHERE hotel_id = ? AND tourist_season_start_date = ? AND tourist_season_end_date = ?",
                (hotel_id, t["tourist_season_start_date"], t["tourist_season_end_date"])
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Tourist season for hotel '{t['hotel_name']}' не знайдено — пропускаємо")
                continue
            tourist_season_id = row[0]

            # --- Отримати hotel_room_type_id ---
            cursor.execute(
                "SELECT hrt.hotel_room_type_id FROM hotel_room_type hrt "
                "JOIN room_type rt ON rt.room_type_id = hrt.room_type_id "
                "WHERE rt.room_type_name = ? AND hrt.hotel_room_type_max_adults = ? AND hrt.hotel_room_type_max_children = ?",
                (t["hotel_room_type_name"], t["max_adults"], t["max_children"])
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Hotel room type '{t['hotel_room_type_name']}' не знайдено — пропускаємо")
                continue
            hotel_room_type_id = row[0]

            # --- Отримати room_price_season_id ---
            cursor.execute(
                "SELECT room_price_season_id FROM room_price_season "
                "WHERE hotel_room_type_id = ? AND tourist_season_id = ?",
                (hotel_room_type_id, tourist_season_id)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Room price season для '{t['hotel_room_type_name']}' не знайдено — пропускаємо")
                continue
            room_price_season_id = row[0]

            # --- Отримати meal_type_id ---
            cursor.execute(
                "SELECT meal_type_id FROM meal_type WHERE meal_type_name = ?",
                (t["meal_type_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Meal type '{t['meal_type_name']}' не знайдено — пропускаємо")
                continue
            meal_type_id = row[0]

            # --- Отримати meal_price_season_id ---
            cursor.execute(
                "SELECT meal_price_season_id FROM meal_price_season "
                "WHERE meal_type_id = ? AND tourist_season_id = ?",
                (meal_type_id, tourist_season_id)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Meal price season для '{t['meal_type_name']}' не знайдено — пропускаємо")
                continue
            meal_price_season_id = row[0]

            # --- Вставка в tour_accommodation ---
            cursor.execute(
                "INSERT INTO tour_accommodation "
                "(room_price_season_id, meal_price_season_id, tour_accommodation_start_date, tour_accommodation_end_date) "
                "VALUES (?, ?, ?, ?)",
                (room_price_season_id, meal_price_season_id, t["tour_accommodation_start_date"], t["tour_accommodation_end_date"])
            )
        conn.commit()
    print(f"✅ Внесено {len(tour_accommodations)} tour accommodations")

# --- Виклик функції ---
insert_tour_accommodations(data.get("tour accommodations", []))
