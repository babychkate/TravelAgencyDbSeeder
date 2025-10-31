import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "hotel_details.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка pricing_policy ---
pricing_policies = data.get("pricing policies", [])

with conn.cursor() as cursor:
    added_count = 0
    for policy in pricing_policies:
        # отримуємо policy_type_id для FK
        cursor.execute(
            "SELECT policy_type_id FROM policy_type WHERE policy_type_name = ?",
            policy["policy_type_name"]
        )
        policy_row = cursor.fetchone()
        if policy_row:
            policy_type_id = policy_row[0]
            cursor.execute(
                """
                INSERT INTO pricing_policy 
                (policy_type_id, accommodation_price_percent, nutrition_price_percent)
                VALUES (?, ?, ?)
                """,
                policy_type_id,
                policy["accommodation_price_percent"],
                policy["nutrition_price_percent"]
            )
            added_count += 1

    conn.commit()
print(f"✅ Внесено {added_count} записів у pricing_policy")
