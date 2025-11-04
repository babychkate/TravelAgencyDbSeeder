import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "hotel_pricing_policies.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def insert_hotel_pricing_policies(policies):
    with conn.cursor() as cursor:
        added_count = 0
        for p in policies:
            # Отримати hotel_id
            cursor.execute("SELECT hotel_id FROM hotel WHERE hotel_name = ?", (p["hotel_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Готель '{p['hotel_name']}' не знайдено — пропускаємо")
                continue
            hotel_id = row[0]

            # Отримати policy_type_id
            cursor.execute("SELECT policy_type_id FROM policy_type WHERE policy_type_name = ?", (p["policy_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Policy '{p['policy_name']}' не знайдено — пропускаємо")
                continue
            pricing_policy_id = row[0]

            # Вставка тільки id
            cursor.execute(
                "INSERT INTO hotel_pricing_policy (hotel_id, pricing_policy_id) VALUES (?, ?)",
                (hotel_id, pricing_policy_id)
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} hotel pricing policies")

# --- Виклик ---
insert_hotel_pricing_policies(data.get("hotel pricing policies", []))
