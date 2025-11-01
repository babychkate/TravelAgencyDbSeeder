import json
from pathlib import Path
from sql_connection import conn

# --- Шлях до JSON ---
file_path = Path(__file__).parent.parent / "data" / "organizations.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Вставка авіаліній ---
airlines = data.get("airlines", [])
with conn.cursor() as cursor:
    count = 0
    for airline in airlines:
        cursor.execute(
            "INSERT INTO airline (airline_name, airline_code) VALUES (?, ?)",
            airline["airline_name"], airline["airline_code"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} авіаліній")

# --- Вставка автобусних компаній ---
bus_companies = data.get("bus companies", [])
with conn.cursor() as cursor:
    count = 0
    for bus in bus_companies:
        cursor.execute(
            "INSERT INTO bus_company (bus_company_name) VALUES (?)",
            bus["bus_company_name"]
        )
        count += 1
    conn.commit()
print(f"✅ Внесено {count} автобусних компаній")
