import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "hotel_relations.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 1. Вставка hotel facilities ---
hotel_facilities = data.get("hotel facilities", [])

with conn.cursor() as cursor:
    count = 0
    for hf in hotel_facilities:
        # отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            hf["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            continue
        hotel_id = hotel_row[0]

        # отримуємо facility_id
        cursor.execute(
            "SELECT facility_id FROM facility WHERE facility_name = ?",
            hf["facility_name"]
        )
        facility_row = cursor.fetchone()
        if not facility_row:
            continue
        facility_id = facility_row[0]

        # вставка в hotel_facility
        cursor.execute(
            """
            INSERT INTO hotel_facility
            (hotel_id, facility_id, hotel_facility_is_paid)
            VALUES (?, ?, ?)
            """,
            hotel_id, facility_id, hf["hotel_facility_is_paid"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} hotel facilities")


# --- Вставка hotel nearby objects (новий формат) ---
nearby_objects = data.get("hotel nearby objects", [])

with conn.cursor() as cursor:
    count = 0
    for obj in nearby_objects:
        # отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            obj["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            continue
        hotel_id = hotel_row[0]

        # отримуємо nearby_object_id за назвою
        cursor.execute(
            "SELECT nearby_object_id FROM nearby_object WHERE nearby_object_name = ?",
            obj["nearby_object_name"]
        )
        object_row = cursor.fetchone()
        if not object_row:
            continue
        nearby_object_id = object_row[0]

        # значення для додаткових полів
        distance_km = obj.get("from_hotel_to_object_distance_km", None)
        transport_min = obj.get("time_to_object_by_transport_min", None)
        walk_min = obj.get("time_to_object_by_walk_min", None)

        # вставка в nearby_object_location
        cursor.execute(
            """
            INSERT INTO nearby_object_location
            (hotel_id, nearby_object_id, from_hotel_to_object_distance_km, time_to_object_by_transport_min, time_to_object_by_walk_min)
            VALUES (?, ?, ?, ?, ?)
            """,
            hotel_id, nearby_object_id, distance_km, transport_min, walk_min
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} записів у nearby_object_location")


# --- 3. Вставка hotel pricing policies ---
hotel_policies = data.get("hotel pricing policies", [])

with conn.cursor() as cursor:
    count = 0
    for policy in hotel_policies:
        # отримуємо hotel_id
        cursor.execute(
            "SELECT hotel_id FROM hotel WHERE hotel_name = ?",
            policy["hotel_name"]
        )
        hotel_row = cursor.fetchone()
        if not hotel_row:
            continue
        hotel_id = hotel_row[0]

        # отримуємо pricing_policy_id
        cursor.execute(
            "SELECT pricing_policy_id FROM pricing_policy pp JOIN policy_type pt ON pp.policy_type_id = pt.policy_type_id WHERE pt.policy_type_name = ?",
            policy["policy_name"]
        )
        policy_row = cursor.fetchone()
        if not policy_row:
            continue
        pricing_policy_id = policy_row[0]

        # вставка в hotel_pricing_policy
        cursor.execute(
            "INSERT INTO hotel_pricing_policy (hotel_id, pricing_policy_id) VALUES (?, ?)",
            hotel_id, pricing_policy_id
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} hotel pricing policies")
