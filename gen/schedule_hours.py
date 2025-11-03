import json
from datetime import datetime, timedelta
from pathlib import Path

# === Шляхи до файлів ===
base_path = Path(__file__).parent.parent
routes_file = base_path / "out" / "routes.json"
output_file = base_path / "out" / "schedule_hours.json"

# === Завантажуємо маршрути ===
with open(routes_file, "r", encoding="utf-8") as f:
    routes_data = json.load(f)

bus_routes = routes_data.get("bus trip routes", [])
flight_routes = routes_data.get("flight routes", [])
all_routes = bus_routes + flight_routes

# === Функція форматування часу ===
def format_time(hour, minute):
    return f"{hour:02d}:{minute:02d}"

# === Генерація schedule_hours ===
schedule_hours = []

for route in all_routes:
    if "departure_bus_station_name" in route:
        dep_time = route.get("departure_time")
        arr_time = route.get("arrival_time")
    else:
        dep_time = route.get("departure_time")
        arr_time = route.get("arrival_time")

    # Якщо часи порожні, можна генерувати випадково (якщо хочеш)
    if not dep_time or not arr_time:
        dep_hour = 6
        dep_minute = 0
        dep_time = format_time(dep_hour, dep_minute)
        arr_time = format_time((dep_hour + 2) % 24, dep_minute)  # простий варіант

    schedule_hours.append({
        "schedule_departure_time": dep_time,
        "schedule_arrival_time": arr_time,
    })

# === Прибираємо дублікати ===
unique_hours = [dict(t) for t in {tuple(sorted(d.items())) for d in schedule_hours}]

# === Збереження ===
output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"schedule hours": unique_hours}, f, ensure_ascii=False, indent=2)

print(f"✅ Згенеровано {len(unique_hours)} записів для schedule_hours")
