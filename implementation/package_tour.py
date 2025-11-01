import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "package_tour.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

package_tours = data.get("package_tours", [])

with conn.cursor() as cursor:
    added_count = 0
    for pt in package_tours:
        # Отримуємо tour_operator_id
        cursor.execute(
            "SELECT tour_operator_id FROM tour_operator WHERE tour_operator_name = ?",
            pt["tour_operator_name"]
        )
        operator_row = cursor.fetchone()
        if not operator_row:
            continue
        tour_operator_id = operator_row[0]

        # Отримуємо package_tour_status_id
        cursor.execute(
            "SELECT package_tour_status_id FROM package_tour_status WHERE package_tour_status_name = ?",
            pt["package_tour_status_name"]
        )
        status_row = cursor.fetchone()
        if not status_row:
            continue
        package_tour_status_id = status_row[0]

        ta = pt["tour_accommodation"]

        # Отримуємо tour_accommodation_id через JOIN на room_type та meal_type
        cursor.execute(
            """
            SELECT ta.tour_accommodation_id
            FROM tour_accommodation ta
            JOIN room_price_season rps
              ON ta.room_price_season_id = rps.room_price_season_id
            JOIN hotel_room_type hrt
              ON rps.hotel_room_type_id = hrt.hotel_room_type_id
            JOIN room_type rt
              ON hrt.room_type_id = rt.room_type_id
            JOIN meal_price_season mps
              ON ta.meal_price_season_id = mps.meal_price_season_id
            JOIN meal_type mt
              ON mps.meal_type_id = mt.meal_type_id
            JOIN tourist_season ts
              ON rps.tourist_season_id = ts.tourist_season_id
            JOIN hotel h
              ON ts.hotel_id = h.hotel_id
            WHERE h.hotel_name = ?
              AND ts.tourist_season_start_date = ?
              AND ts.tourist_season_end_date = ?
              AND rt.room_type_name = ?
              AND hrt.hotel_room_type_max_adults = ?
              AND hrt.hotel_room_type_max_children = ?
              AND mt.meal_type_name = ?
            """,
            ta["hotel_name"],
            ta["tourist_season_start_date"],
            ta["tourist_season_end_date"],
            ta["hotel_room_type_name"],
            ta["max_adults"],
            ta["max_children"],
            ta["meal_type_name"]
        )
        tour_accommodation_row = cursor.fetchone()
        if not tour_accommodation_row:
            print(f"⚠️ Пропущено: не знайдено tour_accommodation для {ta['hotel_name']}")
            continue
        tour_accommodation_id = tour_accommodation_row[0]

        # Вставка в package_tour
        cursor.execute(
            """
            INSERT INTO package_tour
            (tour_operator_id, tour_accommodation_id, package_tour_status_id,
             package_tour_name, package_tour_description,
             package_tour_start_date, package_tour_end_date, package_tour_max_tourists_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tour_operator_id,
            tour_accommodation_id,
            package_tour_status_id,
            pt["package_tour_name"],
            pt["package_tour_description"],
            pt["package_tour_start_date"],
            pt["package_tour_end_date"],
            pt["package_tour_max_tourists_count"]
        )
        added_count += 1

    conn.commit()

print(f"✅ Внесено {added_count} записів у package_tour")
