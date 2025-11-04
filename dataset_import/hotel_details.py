import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotel_details.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка room beds ---
def insert_room_beds(room_beds):
    with conn.cursor() as cursor:
        for bed in room_beds:
            cursor.execute(
                "SELECT bed_type_id FROM bed_type WHERE bed_type_name = ?",
                (bed["bed_type_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Bed type '{bed['bed_type_name']}' не знайдено — пропускаємо")
                continue
            bed_type_id = row[0]

            cursor.execute(
                "INSERT INTO room_bed (bed_type_id, room_bed_quantity) VALUES (?, ?)",
                (bed_type_id, bed["room_bed_quantity"])
            )
        conn.commit()
    print(f"✅ Внесено {len(room_beds)} room beds")

# --- Вставка hotel room types ---
def insert_hotel_room_types(room_types):
    with conn.cursor() as cursor:
        for r in room_types:
            # Отримати room_type_id з таблиці room_type
            cursor.execute(
                "SELECT room_type_id FROM room_type WHERE room_type_name = ?",
                (r["hotel_room_type_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Room type '{r['hotel_room_type_name']}' не знайдено — пропускаємо")
                continue
            room_type_id = row[0]

            cursor.execute(
                "INSERT INTO hotel_room_type (room_type_id, hotel_room_type_max_adults, hotel_room_type_max_children) VALUES (?, ?, ?)",
                (room_type_id, r["max_adults"], r["max_children"])
            )
        conn.commit()
    print(f"✅ Внесено {len(room_types)} hotel room types")

# --- Вставка hotel room type beds ---
def insert_hotel_room_type_beds(room_type_beds):
    with conn.cursor() as cursor:
        for rtb in room_type_beds:
            # Отримати hotel_room_type_id
            cursor.execute(
                """
                SELECT hrt.hotel_room_type_id 
                FROM hotel_room_type hrt
                JOIN room_type rt ON hrt.room_type_id = rt.room_type_id
                WHERE rt.room_type_name = ? AND hrt.hotel_room_type_max_adults = ? AND hrt.hotel_room_type_max_children = ?
                """,
                (rtb["hotel_room_type_name"], rtb["hotel_room_type_max_adults"], rtb["hotel_room_type_max_children"])
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Hotel room type '{rtb['hotel_room_type_name']}' не знайдено — пропускаємо")
                continue
            hotel_room_type_id = row[0]

            # Отримати room_bed_id
            cursor.execute(
                "SELECT room_bed_id FROM room_bed rb JOIN bed_type bt ON rb.bed_type_id = bt.bed_type_id WHERE bt.bed_type_name = ?",
                (rtb["bed_type_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Bed '{rtb['bed_type_name']}' не знайдено — пропускаємо")
                continue
            room_bed_id = row[0]

            cursor.execute(
                "INSERT INTO hotel_room_type_bed (hotel_room_type_id, room_bed_id) VALUES (?, ?)",
                (hotel_room_type_id, room_bed_id)
            )
        conn.commit()
    print(f"✅ Внесено {len(room_type_beds)} hotel room type beds")

# --- Вставка pricing policies ---
def insert_pricing_policies(policies):
    with conn.cursor() as cursor:
        for p in policies:
            cursor.execute(
                "SELECT policy_type_id FROM policy_type WHERE policy_type_name = ?",
                (p["policy_type_name"],)
            )
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Policy type '{p['policy_type_name']}' не знайдено — пропускаємо")
                continue
            policy_type_id = row[0]

            cursor.execute(
                "INSERT INTO pricing_policy (policy_type_id, accommodation_price_percent, nutrition_price_percent) VALUES (?, ?, ?)",
                (policy_type_id, p["accommodation_price_percent"], p["nutrition_price_percent"])
            )
        conn.commit()
    print(f"✅ Внесено {len(policies)} pricing policies")

# --- Виклики функцій ---
insert_room_beds(data.get("room beds", []))
insert_hotel_room_types(data.get("hotel room types", []))
insert_hotel_room_type_beds(data.get("hotel room type beds", []))
insert_pricing_policies(data.get("pricing policies", []))