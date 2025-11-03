import json
import random

# --- Зчитування сезонів ---
with open("out/seasons.json", "r", encoding="utf-8") as f:
    seasons_data = json.load(f)
    bus_seasons = seasons_data.get("bus seasons", [])
    flight_seasons = seasons_data.get("flight seasons", [])

# --- Зчитування розкладу ---
with open("out/schedules.json", "r", encoding="utf-8") as f:
    schedules_data = json.load(f)
    bus_schedules = schedules_data.get("bus schedules", [])
    flight_schedules = schedules_data.get("flight schedules", [])

# --- Функція генерації проміжної таблиці ---
def generate_schedule_assignments(seasons, schedules, avg_per_season=3):
    assignments = []
    for season in seasons:
        route_number = season["route_number"]
        season_start = season["season_start_date"]
        season_end = season["season_end_date"]
        
        # Вибираємо випадково 3 (або avg_per_season) розклади для сезону
        selected_schedules = random.sample(schedules, k=min(avg_per_season, len(schedules)))
        
        for sched in selected_schedules:
            assignments.append({
                "route_number": route_number,
                "season_start_date": season_start,
                "season_end_date": season_end,
                "schedule_day_name": sched["schedule_day_name"],
                "schedule_departure_time": sched["schedule_departure_time"],
                "schedule_arrival_time": sched["schedule_arrival_time"]
            })
    return assignments

# --- Генерація для автобусів та авіа ---
bus_assignments = generate_schedule_assignments(bus_seasons, bus_schedules)
flight_assignments = generate_schedule_assignments(flight_seasons, flight_schedules)

# --- Збереження ---
with open("out/season_schedule_assignments.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus assignments": bus_assignments,
        "flight assignments": flight_assignments
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_assignments)} автобусних та {len(flight_assignments)} авіаційних прив'язок сезону до розкладу")
