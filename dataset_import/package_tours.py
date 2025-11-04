import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "package_tours.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with conn.cursor() as cursor:
    package_tour_counter = 0
    for tour in data["package tours"]:
        # --- Tour Operator ---
        tour_operator = tour["tour_operator_name"]
        cursor.execute(
            "SELECT tour_operator_id FROM tour_operator WHERE tour_operator_name = ?",
            (tour_operator["tour_operator_name"],)
        )
        row = cursor.fetchone()
        if row:
            tour_operator_id = row[0]
        else:
            print(f" Tour operator not found: {tour_operator['tour_operator_name']}")
            continue

        # --- Hotel ---
        accommodation = tour["tour_accommodation"]
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            (accommodation["hotel_name"],)
        )
        row = cursor.fetchone()
        if row:
            hotel_id = row[0]
        else:
            print(f" Hotel not found: {accommodation['hotel_name']}")
            continue

        # --- Tourist Season ---
        cursor.execute(
            "SELECT tourist_season_id FROM tourist_season WHERE hotel_id = ? AND tourist_season_start_date = ? AND tourist_season_end_date = ?",
            (hotel_id, accommodation["tourist_season_start_date"], accommodation["tourist_season_end_date"])
        )
        row = cursor.fetchone()
        if row:
            tourist_season_id = row[0]
        else:
            print(f" Tourist season not found: {accommodation['tourist_season_start_date']} - {accommodation['tourist_season_end_date']}")
            continue

        # --- Room Type ---
        room_type_name = accommodation["hotel_room_type_name"]
        cursor.execute(
            "SELECT room_type_id FROM room_type WHERE room_type_name = ?",
            (room_type_name,)
        )
        row = cursor.fetchone()
        if row:
            room_type_id = row[0]
        else:
            print(f" Room type not found: {room_type_name}")
            continue

        # --- Hotel Room Type ---
        cursor.execute(
            """SELECT hotel_room_type_id FROM hotel_room_type 
               WHERE room_type_id = ? AND hotel_room_type_max_adults = ? AND hotel_room_type_max_children = ?""",
            (room_type_id, accommodation["max_adults"], accommodation["max_children"])
        )
        row = cursor.fetchone()
        if row:
            hotel_room_type_id = row[0]
        else:
            print(f" Hotel room type not found for {room_type_name}, adults {accommodation['max_adults']}, children {accommodation['max_children']}")
            continue

        # --- Room Price Season ---
        cursor.execute(
            """SELECT room_price_season_id FROM room_price_season 
               WHERE hotel_room_type_id = ? AND tourist_season_id = ?""",
            (hotel_room_type_id, tourist_season_id)
        )
        row = cursor.fetchone()
        if row:
            room_price_season_id = row[0]
        else:
            print(f" Room price season not found for hotel_room_type_id {hotel_room_type_id} and tourist_season_id {tourist_season_id}")
            continue

        # --- Meal Type ---
        meal_type_name = accommodation["meal_type_name"]
        cursor.execute(
            "SELECT meal_type_id FROM meal_type WHERE meal_type_name = ?",
            (meal_type_name,)
        )
        row = cursor.fetchone()
        if row:
            meal_type_id = row[0]
        else:
            print(f" Meal type not found: {meal_type_name}")
            continue

        # --- Meal Price Season ---
        cursor.execute(
            """SELECT meal_price_season_id FROM meal_price_season 
               WHERE meal_type_id = ? AND tourist_season_id = ?""",
            (meal_type_id, tourist_season_id)
        )
        row = cursor.fetchone()
        if row:
            meal_price_season_id = row[0]
        else:
            print(f" Meal price season not found for meal_type_id {meal_type_id} and tourist_season_id {tourist_season_id}")
            continue

        # --- Tour Accommodation ---
        cursor.execute(
            """SELECT tour_accommodation_id FROM tour_accommodation 
               WHERE room_price_season_id = ? AND tour_accommodation_start_date = ? AND tour_accommodation_end_date = ?""",
            (room_price_season_id, accommodation["tour_accommodation_start_date"], accommodation["tour_accommodation_end_date"])
        )
        row = cursor.fetchone()
        if row:
            tour_accommodation_id = row[0]
        else:
            print(f" Tour accommodation not found: {accommodation['tour_accommodation_start_date']} - {accommodation['tour_accommodation_end_date']}")
            continue

        # --- Package Tour Status ---
        package_tour_status_name = tour["package_tour_status_name"]
        cursor.execute(
            "SELECT package_tour_status_id FROM package_tour_status WHERE package_tour_status_name = ?",
            (package_tour_status_name,)
        )
        row = cursor.fetchone()
        if row:
            package_tour_status_id = row[0]
        else:
            print(f" Package tour status not found: {package_tour_status_name}")
            continue
        
        package_tour_counter =  package_tour_counter + 1

        # --- Package Tour ---
    print(f"✅ Було внесено {package_tour_counter} пактних турів")
