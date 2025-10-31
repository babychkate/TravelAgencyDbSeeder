import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування згенерованих автобусних маршрутів ---
with open(base_path / "output/bus_trip_route.json", "r", encoding="utf-8") as f:
    bus_trip_routes = json.load(f)["bus trip routes"]

# --- Зчитування сезонів ---
with open(base_path / "output/bus_trip_season.json", "r", encoding="utf-8") as f:
    bus_trip_seasons = json.load(f)["bus trip seasons"]

# --- Зчитування розкладу ---
with open(base_path / "data/schedules.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)["schedule"]

# --- Генерація проміжної таблиці ---
bus_trip_season_schedules = []

for season in bus_trip_seasons:
    route_number = season["route_number"]
    start_date = season["bus_trip_season_start_date"]
    end_date = season["bus_trip_season_end_date"]
    
    # беремо 3 випадкові розклади з масиву schedule
    sample_schedules = random.sample(schedule, 3)
    
    for s in sample_schedules:
        bus_trip_season_schedules.append({
            "route_number": route_number,
            "bus_trip_season_start_date": start_date,
            "bus_trip_season_end_date": end_date,
            "schedule_departure_time": s["schedule_departure_time"],
            "schedule_arrival_time": s["schedule_arrival_time"],
            "day_name": s["schedule_day_name"]
        })

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "bus_trip_season_schedule.json", "w", encoding="utf-8") as f:
    json.dump({"bus trip season schedules": bus_trip_season_schedules}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_trip_season_schedules)} записів у bus_trip_season_schedule")
