import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування згенерованих авіарейсів ---
with open(base_path / "output/flight_route.json", "r", encoding="utf-8") as f:
    flight_routes = json.load(f)["flight routes"]

# --- Зчитування сезонів ---
with open(base_path / "output/flight_season.json", "r", encoding="utf-8") as f:
    flight_seasons = json.load(f)["flight seasons"]

# --- Зчитування розкладу ---
with open(base_path / "data/schedules.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)["schedule"]

# --- Генерація проміжної таблиці ---
flight_season_schedules = []

for season in flight_seasons:
    route_number = season["route_number"]
    start_date = season["flight_trip_season_start_date"]
    end_date = season["flight_trip_season_end_date"]
    
    # беремо 3 випадкові розклади з масиву schedule
    sample_schedules = random.sample(schedule, 3)
    
    for s in sample_schedules:
        flight_season_schedules.append({
            "route_number": route_number,
            "flight_trip_season_start_date": start_date,
            "flight_trip_season_end_date": end_date,
            "schedule_departure_time": s["schedule_departure_time"],
            "schedule_arrival_time": s["schedule_arrival_time"],
            "day_name": s["schedule_day_name"]
        })

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "flight_season_schedule.json", "w", encoding="utf-8") as f:
    json.dump({"flight season schedules": flight_season_schedules}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(flight_season_schedules)} записів у flight_season_schedule")
