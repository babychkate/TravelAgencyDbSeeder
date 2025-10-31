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
flight_route_types = [t.get("flight_route_type_name") 
                      for t in classifiers.get("flight route types", [])]
if not flight_route_types:
    flight_route_types = ["Regular", "Charter", "Night"]

airports = [a.get("airport_name") 
            for a in geography.get("airports", [])]
if not airports:
    airports = [f"Airport {i+1}" for i in range(5)]

airlines = [a.get("airline_name") 
            for a in organizations.get("airlines", [])]
if not airlines:
    airlines = [f"Airline {i+1}" for i in range(4)]

# --- Генерація 40 авіарейсів ---
flight_routes = []
for i in range(1, 41):
    departure, arrival = random.sample(airports, 2)
    duration_hours = random.randint(1, 6)
    duration_minutes = random.choice([0, 15, 30, 45])
    duration = f"{duration_hours:02d}:{duration_minutes:02d}:00"

    flight_routes.append({
        "flight_number": f"F-{i:05d}",
        "flight_duration": duration,
        "flight_route_type_name": random.choice(flight_route_types),
        "departure_airport_name": departure,
        "arrival_airport_name": arrival,
        "airline_name": random.choice(airlines)
    })

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "flight_route.json", "w", encoding="utf-8") as f:
    json.dump({"flight routes": flight_routes}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(flight_routes)} авіарейсів")
