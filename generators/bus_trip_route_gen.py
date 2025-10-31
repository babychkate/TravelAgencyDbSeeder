import json
import random
from pathlib import Path

# --- Базовий шлях ---
base_path = Path(__file__).parent.parent

# --- Зчитування класифікаторів ---
with open(base_path / "data/classifiers.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

with open(base_path / "data/geography.json", "r", encoding="utf-8") as f:
    geography = json.load(f)

with open(base_path / "data/organizations.json", "r", encoding="utf-8") as f:
    organizations = json.load(f)

# --- Підготовка даних ---
bus_route_types = [t.get("bus_trip_route_type_name") 
                   for t in classifiers.get("bus trip route types", [])]
if not bus_route_types:
    bus_route_types = ["Day", "Night", "Express"]

bus_stations = [s.get("bus_station_name") 
                for s in geography.get("bus stations", [])]
if not bus_stations:
    bus_stations = [f"Station {i+1}" for i in range(5)]

bus_companies = [c.get("bus_company_name") 
                 for c in organizations.get("bus companies", [])]
if not bus_companies:
    bus_companies = [f"Company {i+1}" for i in range(4)]

# --- Генерація 40 маршрутів ---
bus_trip_routes = []
for i in range(1, 41):
    departure, arrival = random.sample(bus_stations, 2)
    duration_hours = random.randint(3, 12)
    duration_minutes = random.choice([0, 15, 30, 45])
    duration = f"{duration_hours:02d}:{duration_minutes:02d}:00"

    bus_trip_routes.append({
        "route_number": f"R-{i:05d}",
        "bus_trip_duration": duration,
        "bus_trip_route_type_name": random.choice(bus_route_types),
        "departure_bus_station_name": departure,
        "arrival_bus_station_name": arrival,
        "bus_company_name": random.choice(bus_companies)
    })

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "bus_trip_route.json", "w", encoding="utf-8") as f:
    json.dump({"bus trip routes": bus_trip_routes}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_trip_routes)} автобусних маршрутів")
