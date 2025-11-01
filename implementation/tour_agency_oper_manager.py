import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "organizations.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- 2️⃣ Вставка туроператорів ---
tour_operators = data.get("tour operators", [])
with conn.cursor() as cursor:
    count = 0
    for operator in tour_operators:
        cursor.execute(
            "INSERT INTO tour_operator (tour_operator_name, tour_operator_description) VALUES (?, ?)",
            operator["tour_operator_name"], operator["tour_operator_description"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} туроператорів")

# --- 3️⃣ Вставка турагенцій ---
travel_agencies = data.get("travel agencies", [])
with conn.cursor() as cursor:
    count = 0
    for agency in travel_agencies:
        # отримуємо city_id для FK
        cursor.execute(
            "SELECT city_id FROM city WHERE city_name = ?",
            agency["travel_agency_city_name"]
        )
        city_row = cursor.fetchone()
        if not city_row:
            continue
        city_id = city_row[0]

        cursor.execute(
            """
            INSERT INTO travel_agency 
            (travel_agency_city_id, travel_agency_name, travel_agency_address, travel_agency_code)
            VALUES (?, ?, ?, ?)
            """,
            city_id, agency["travel_agency_name"], agency["travel_agency_address"], agency["travel_agency_code"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} турагенцій")

# --- 4️⃣ Вставка менеджерів турагенцій ---
travel_managers = data.get("travel agency managers", [])
with conn.cursor() as cursor:
    count = 0
    for manager in travel_managers:
        # отримуємо travel_agency_id для FK
        cursor.execute(
            "SELECT travel_agency_id FROM travel_agency WHERE travel_agency_name = ?",
            manager["travel_agency_name"]
        )
        agency_row = cursor.fetchone()
        if not agency_row:
            continue
        travel_agency_id = agency_row[0]

        cursor.execute(
            """
            INSERT INTO travel_agency_manager
            (travel_agency_id, travel_agency_manager_full_name, travel_agency_manager_email)
            VALUES (?, ?, ?)
            """,
            travel_agency_id, manager["travel_manager_full_name"], manager["travel_agency_manager_email"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} менеджерів турагенцій")
