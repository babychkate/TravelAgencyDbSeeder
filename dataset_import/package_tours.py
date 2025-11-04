import json
from pathlib import Path
from sql_connection import conn  # твоє підключення pyodbc

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
            cursor.execute(
                "INSERT INTO tour_operator (tour_operator_name, tour_operator_description) VALUES (?, ?); SELECT SCOPE_IDENTITY()",
                (tour_operator["tour_operator_name"], tour_operator.get("tour_operator_description", ""))
            )
            tour_operator_id = cursor.fetchone()[0]

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
            cursor.execute(
                "INSERT INTO hotel (hotel_name) VALUES (?); SELECT SCOPE_IDENTITY()",
                (accommodation["hotel_name"],)
            )
            hotel_id = cursor.fetchone()[0]

        # --- Tourist Season ---
        cursor.execute(
            "SELECT tourist_season_id FROM tourist_season WHERE hotel_id = ? AND tourist_season_start_date = ? AND tourist_season_end_date = ?",
            (hotel_id, accommodation["tourist_season_start_date"], accommodation["tourist_season_end_date"])
        )
        row = cursor.fetchone()
        if row:
            tourist_season_id = row[0]
        else:
            cursor.execute(
                """INSERT INTO tourist_season (hotel_id, tourist_season_start_date, tourist_season_end_date)
                   VALUES (?, ?, ?); SELECT SCOPE_IDENTITY()""",
                (hotel_id, accommodation["tourist_season_start_date"], accommodation["tourist_season_end_date"])
            )
            tourist_season_id = cursor.fetchone()[0]

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
            cursor.execute(
                "INSERT INTO room_type (room_type_name) VALUES (?); SELECT SCOPE_IDENTITY()",
                (room_type_name,)
            )
            room_type_id = cursor.fetchone()[0]

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
            cursor.execute(
                """INSERT INTO hotel_room_type (room_type_id, hotel_room_type_max_adults, hotel_room_type_max_children)
                   VALUES (?, ?, ?); SELECT SCOPE_IDENTITY()""",
                (room_type_id, accommodation["max_adults"], accommodation["max_children"])
            )
            hotel_room_type_id = cursor.fetchone()[0]

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
            cursor.execute(
                """INSERT INTO room_price_season (hotel_room_type_id, tourist_season_id, room_price_per_person)
                   VALUES (?, ?, ?); SELECT SCOPE_IDENTITY()""",
                (hotel_room_type_id, tourist_season_id, accommodation["total_price_per_person"])
            )
            room_price_season_id = cursor.fetchone()[0]

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
            cursor.execute(
                "INSERT INTO meal_type (meal_type_name) VALUES (?); SELECT SCOPE_IDENTITY()",
                (meal_type_name,)
            )
            meal_type_id = cursor.fetchone()[0]

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
            cursor.execute(
                """INSERT INTO meal_price_season (meal_type_id, tourist_season_id, meal_price_per_person)
                   VALUES (?, ?, ?); SELECT SCOPE_IDENTITY()""",
                (meal_type_id, tourist_season_id, accommodation["total_price_per_person"])
            )
            meal_price_season_id = cursor.fetchone()[0]

        # --- Tour Accommodation ---
        cursor.execute(
            """SELECT tour_accommodation_id FROM tour_accommodation 
               WHERE tour_accommodation_start_date = ? AND tour_accommodation_end_date = ?""",
            (accommodation["tour_accommodation_start_date"], accommodation["tour_accommodation_end_date"])
        )
        row = cursor.fetchone()
        if row:
            tour_accommodation_id = row[0]
        else:
            cursor.execute(
                """INSERT INTO tour_accommodation (room_price_season_id, meal_price_season_id, tour_accommodation_start_date, tour_accommodation_end_date)
                   VALUES (?, ?, ?, ?); SELECT SCOPE_IDENTITY()""",
                (room_price_season_id, meal_price_season_id, accommodation["tour_accommodation_start_date"], accommodation["tour_accommodation_end_date"])
            )
            tour_accommodation_id = cursor.fetchone()[0]

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
            cursor.execute(
                "INSERT INTO package_tour_status (package_tour_status_name) VALUES (?); SELECT SCOPE_IDENTITY()",
                (package_tour_status_name,)
            )
            package_tour_status_id = cursor.fetchone()[0]

        # --- Package Tour ---
        cursor.execute(
            """INSERT INTO package_tour (
                tour_operator_id,
                tour_accommodation_id,
                package_tour_status_id,
                package_tour_name,
                package_tour_description,
                package_tour_start_date,
                package_tour_end_date,
                package_tour_max_tourists_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                tour_operator_id,
                tour_accommodation_id,
                package_tour_status_id,
                tour["package_tour_name"],
                tour["package_tour_description"],
                tour["package_tour_start_date"],
                tour["package_tour_end_date"],
                tour["package_tour_max_tourists_count"]
            )
        )
        package_tour_counter =  package_tour_counter + 1

    conn.commit()
print(f"✅ Було внесено {package_tour_counter} пактних турів")
