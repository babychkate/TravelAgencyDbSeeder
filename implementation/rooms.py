import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "hotel_details.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Вставка room_bed ---
room_beds = data.get("room beds", [])

with conn.cursor() as cursor:
    count = 0
    for bed in room_beds:
        # отримуємо bed_type_id
        cursor.execute(
            "SELECT bed_type_id FROM bed_type WHERE bed_type_name = ?",
            bed["bed_type_name"]
        )
        bed_type_row = cursor.fetchone()
        if not bed_type_row:
            continue
        bed_type_id = bed_type_row[0]

        # вставка в room_bed
        cursor.execute(
            "INSERT INTO room_bed (bed_type_id, room_bed_quantity) VALUES (?, ?)",
            bed_type_id, bed["room_bed_quantity"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} записів у room_bed")


# --- 2. Вставка hotel_room_type ---
hotel_room_types = data.get("hotel room types", [])

with conn.cursor() as cursor:
    count = 0
    for room_type in hotel_room_types:
        # отримуємо room_type_id за назвою типу кімнати
        cursor.execute(
            "SELECT room_type_id FROM room_type WHERE room_type_name = ?",
            room_type["hotel_room_type_name"]
        )
        room_type_row = cursor.fetchone()
        if not room_type_row:
            continue
        room_type_id = room_type_row[0]

        cursor.execute(
            """
            INSERT INTO hotel_room_type
            (room_type_id, hotel_room_type_max_adults, hotel_room_type_max_children)
            VALUES (?, ?, ?)
            """,
            room_type_id,
            room_type["max_adults"],
            room_type["max_children"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} записів у hotel_room_type")


# --- 3. Вставка hotel_room_type_bed ---
hotel_room_type_beds = data.get("hotel room type beds", [])

with conn.cursor() as cursor:
    count = 0
    for link in hotel_room_type_beds:
        # отримуємо hotel_room_type_id
        cursor.execute(
            """
            SELECT hrt.hotel_room_type_id
            FROM hotel_room_type hrt
            JOIN room_type rt ON hrt.room_type_id = rt.room_type_id
            WHERE rt.room_type_name = ?
              AND hrt.hotel_room_type_max_adults = ?
              AND hrt.hotel_room_type_max_children = ?
            """,
            link["hotel_room_type_name"],
            link["hotel_room_type_max_adults"],
            link["hotel_room_type_max_children"]
        )
        room_type_row = cursor.fetchone()
        if not room_type_row:
            continue
        hotel_room_type_id = room_type_row[0]

        # отримуємо room_bed_id
        cursor.execute(
            """
            SELECT rb.room_bed_id
            FROM room_bed rb
            JOIN bed_type bt ON rb.bed_type_id = bt.bed_type_id
            WHERE bt.bed_type_name = ?
            """,
            link["bed_type_name"]
        )
        bed_row = cursor.fetchone()
        if not bed_row:
            continue
        room_bed_id = bed_row[0]

        # вставка в hotel_room_type_bed
        cursor.execute(
            "INSERT INTO hotel_room_type_bed (room_bed_id, hotel_room_type_id) VALUES (?, ?)",
            room_bed_id, hotel_room_type_id
        )
        count += 1
    conn.commit()
    print(f"✅ Внесено {count} записів у hotel_room_type_bed")
