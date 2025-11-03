import json
import random

# --- Зчитуємо сезони ---
with open("out/seasons.json", "r", encoding="utf-8") as f:
    seasons_data = json.load(f)
    bus_seasons = seasons_data.get("bus seasons", [])
    flight_seasons = seasons_data.get("flight seasons", [])

# --- Зчитуємо розклад ---
with open("in/schedules.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)["schedules"]  # або як у тебе називається

# --- Генерація season schedules для автобусів ---
bus_season_schedules = []
for season in bus_seasons:
    route_number = season["route_number"]
    sample_schedules = random.sample(schedule, 3)
    for s in sample_schedules:
        bus_season_schedules.append({
            "route_number": route_number,
            "season_start_date": season["season_start_date"],
            "season_end_date": season["season_end_date"],
            "schedule_departure_time": s["schedule_departure_time"],
            "schedule_arrival_time": s["schedule_arrival_time"],
            "day_name": s["schedule_day_name"]
        })

# --- Генерація season schedules для літаків ---
flight_season_schedules = []
for season in flight_seasons:
    route_number = season["route_number"]
    sample_schedules = random.sample(schedule, 3)
    for s in sample_schedules:
        flight_season_schedules.append({
            "route_number": route_number,
            "season_start_date": season["season_start_date"],
            "season_end_date": season["season_end_date"],
            "schedule_departure_time": s["schedule_departure_time"],
            "schedule_arrival_time": s["schedule_arrival_time"],
            "day_name": s["schedule_day_name"]
        })

# --- Зберігаємо ---
with open("out/season_schedules.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus season schedules": bus_season_schedules,
        "flight season schedules": flight_season_schedules
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_season_schedules)} записів для автобусів та {len(flight_season_schedules)} записів для літаків.")
