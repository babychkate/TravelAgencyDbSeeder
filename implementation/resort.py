import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "geography.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

resorts = data.get("resorts", [])

with conn.cursor() as cursor:
    for resort in resorts:
        # --- отримуємо country_id ---
        cursor.execute(
            "SELECT country_id FROM country WHERE country_name = ?",
            resort["country_name"]
        )
        country_id = cursor.fetchone()[0]

        # --- отримуємо vacation_type_id ---
        cursor.execute(
            "SELECT vacation_type_id FROM vacation_type WHERE vacation_type_name = ?",
            resort["vacation_type_name"]
        )
        vacation_type_id = cursor.fetchone()[0]

        # --- вставка запису ---
        cursor.execute(
            """INSERT INTO resort
               (resort_name, country_id, vacation_type_id, resort_city_tax)
               VALUES (?, ?, ?, ?)""",
            resort["resort_name"], country_id, vacation_type_id, resort["resort_city_tax"]
        )
    conn.commit()

print(f"✅ Внесено {len(resorts)} курортів")
