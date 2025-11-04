import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "package_tours.json"

with open(file_path, "r", encoding="utf-8") as f:
    package_tours = json.load(f)["package tours"]

with conn.cursor() as cursor:
    for tour in package_tours:
        # --- Tour operator ---
        operator_name = tour["tour_operator_name"]["tour_operator_name"]
        operator_description = tour["tour_operator_name"].get("tour_operator_description", "")

        cursor.execute("""
            SELECT tour_operator_id
            FROM tour_operator
            WHERE tour_operator_name = ?
        """, (operator_name,))
        operator_row = cursor.fetchone()
        if operator_row:
            tour_operator_id = operator_row[0]
        else:
            cursor.execute("""
                INSERT INTO tour_operator (tour_operator_name, tour_operator_description)
                VALUES (?, ?)
            """, (operator_name, operator_description))
            tour_operator_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

        # --- Room type ---
        room_type_name = tour["tour_accommodation"]["hotel_room_type_name"]
        max_adults = tour["tour_accommodation"]["max_adults"]
        max_children = tour["tour_accommodation"]["max_children"]

        cursor.execute("""
            SELECT room_type_id
            FROM room_type
            WHERE room_type_name = ?
        """, (room_type_name,))
        room_type_row = cursor.fetchone()
        if not room_type_row:
            continue
        room_type_id = room_type_row[0]

        # --- Hotel room type ---
        cursor.execute("""
            SELECT hotel_room_type_id
            FROM hotel_room_type
            WHERE room_type_id = ?
              AND hotel_room_type_max_adults >= ?
              AND hotel_room_type_max_children >= ?
        """, (room_type_id, max_adults, max_children))
        room_row = cursor.fetchone()
        if not room_row:
            continue
        hotel_room_type_id = room_row[0]

        # --- Tourist season ---
        start_date = tour["tour_accommodation"]["tourist_season_start_date"]
        end_date = tour["tour_accommodation"]["tourist_season_end_date"]

        cursor.execute("""
            SELECT tourist_season_id
            FROM tourist_season
            WHERE tourist_season_start_date = ? AND tourist_season_end_date = ?
        """, (start_date, end_date))
        season_row = cursor.fetchone()
        if not season_row:
            continue
        tourist_season_id = season_row[0]

        # --- Tour accommodation ---
        tour_start = tour["tour_accommodation"]["tour_accommodation_start_date"]
        tour_end = tour["tour_accommodation"]["tour_accommodation_end_date"]
        total_price = tour["tour_accommodation"]["total_price_per_person"]

        cursor.execute("""
            SELECT tour_accommodation_id
            FROM tour_accommodation
            WHERE room_price_season_id = ?
              AND tour_accommodation_start_date = ?
              AND tour_accommodation_end_date = ?
        """, (hotel_room_type_id, tour_start, tour_end))
        accom_row = cursor.fetchone()
        if not accom_row:
            continue
        tour_accommodation_id = accom_row[0]

        # --- Package tour status ---
        status_name = tour.get("package_tour_status_name", "Active")
        cursor.execute("""
            SELECT package_tour_status_id
            FROM package_tour_status
            WHERE package_tour_status_name = ?
        """, (status_name,))
        status_row = cursor.fetchone()
        if not status_row:
            continue
        package_tour_status_id = status_row[0]

        # --- Insert package tour ---
        cursor.execute("""
            INSERT INTO package_tour (
                tour_operator_id,
                tour_accommodation_id,
                package_tour_status_id,
                package_tour_name,
                package_tour_description,
                package_tour_start_date,
                package_tour_end_date,
                package_tour_max_tourists_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tour_operator_id,
            tour_accommodation_id,
            package_tour_status_id,
            tour["package_tour_name"],
            tour["package_tour_description"],
            tour["package_tour_start_date"],
            tour["package_tour_end_date"],
            tour["package_tour_max_tourists_count"]
        ))

    conn.commit()
print(f"✅ Внесено {len(package_tours)} package tours")
