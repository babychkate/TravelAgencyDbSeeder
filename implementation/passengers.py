import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "passengers.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка пасажирів ---
passengers = data.get("passengers", [])
with conn.cursor() as cursor:
    count = 0
    for passenger in passengers:
        cursor.execute(
            """
            INSERT INTO passenger
            (passenger_first_name, passenger_last_name, passenger_birth_date, passenger_passport_number)
            VALUES (?, ?, ?, ?)
            """,
            passenger["passenger_first_name"],
            passenger["passenger_last_name"],
            passenger["passenger_birth_date"],
            passenger["passenger_passport_number"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} пасажирів")
