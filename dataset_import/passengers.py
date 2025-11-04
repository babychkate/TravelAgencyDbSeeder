import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "passengers.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка пасажирів ---
def insert_passengers(passengers):
    with conn.cursor() as cursor:
        added_count = 0
        for p in passengers:
            cursor.execute(
                """
                INSERT INTO passenger (passenger_first_name, passenger_last_name, passenger_birth_date, passenger_passport_number)
                VALUES (?, ?, ?, ?)
                """,
                (p["passenger_first_name"], p["passenger_last_name"], p["passenger_birth_date"], p["passenger_passport_number"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} passengers")

# --- Виклик ---
insert_passengers(data.get("passengers", []))
