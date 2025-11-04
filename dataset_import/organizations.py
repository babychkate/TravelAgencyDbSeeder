import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "dataset" / "organizations.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Airlines ---
def insert_airlines(airlines):
    with conn.cursor() as cursor:
        added_count = 0
        for a in airlines:
            cursor.execute(
                "INSERT INTO airline (airline_name, airline_code) VALUES (?, ?)",
                (a["airline_name"], a["airline_code"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} airlines")

# --- Bus Companies ---
def insert_bus_companies(companies):
    with conn.cursor() as cursor:
        added_count = 0
        for c in companies:
            cursor.execute(
                "INSERT INTO bus_company (bus_company_name) VALUES (?)",
                (c["bus_company_name"],)
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} bus companies")

# --- Tour Operators ---
def insert_tour_operators(operators):
    with conn.cursor() as cursor:
        added_count = 0
        for o in operators:
            cursor.execute(
                "INSERT INTO tour_operator (tour_operator_name, tour_operator_description) VALUES (?, ?)",
                (o["tour_operator_name"], o["tour_operator_description"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} tour operators")

# --- Travel Agencies ---
def insert_travel_agencies(agencies):
    with conn.cursor() as cursor:
        added_count = 0
        for a in agencies:
            # Отримати city_id
            cursor.execute("SELECT city_id FROM city WHERE city_name = ?", (a["travel_agency_city_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Місто '{a['travel_agency_city_name']}' не знайдено — пропускаємо")
                continue
            city_id = row[0]

            cursor.execute(
                "INSERT INTO travel_agency (travel_agency_city_id, travel_agency_name, travel_agency_address, travel_agency_code) VALUES (?, ?, ?, ?)",
                (city_id, a["travel_agency_name"], a["travel_agency_address"], a["travel_agency_code"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} travel agencies")

# --- Travel Agency Managers ---
def insert_travel_agency_managers(managers):
    with conn.cursor() as cursor:
        added_count = 0
        for m in managers:
            # Отримати travel_agency_id
            cursor.execute("SELECT travel_agency_id FROM travel_agency WHERE travel_agency_name = ?", (m["travel_agency_name"],))
            row = cursor.fetchone()
            if not row:
                print(f"⚠ Агентство '{m['travel_agency_name']}' не знайдено — пропускаємо")
                continue
            agency_id = row[0]

            cursor.execute(
                "INSERT INTO travel_agency_manager (travel_agency_id, travel_agency_manager_full_name, travel_agency_manager_email) VALUES (?, ?, ?)",
                (agency_id, m["travel_manager_full_name"], m["travel_agency_manager_email"])
            )
            added_count += 1
        conn.commit()
    print(f"✅ Внесено {added_count} travel agency managers")

# --- Виклики ---
insert_airlines(data.get("airlines", []))
insert_bus_companies(data.get("bus companies", []))
insert_tour_operators(data.get("tour operators", []))
insert_travel_agencies(data.get("travel agencies", []))
insert_travel_agency_managers(data.get("travel agency managers", []))
