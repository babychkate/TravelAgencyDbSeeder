import json
import random
from datetime import datetime, timedelta

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

# --- Зчитування маршрутів для duration ---
with open("out/routes.json", "r", encoding="utf-8") as f:
    routes_data = json.load(f)
    bus_routes = {r["route_number"]: r for r in routes_data.get("bus trip routes", [])}
    flight_routes = {r["route_number"]: r for r in routes_data.get("flight routes", [])}

# --- Допоміжна функція для перевірки duration ---
def is_schedule_matching_duration(schedule, route, trip_type="bus"):
    dep_time = datetime.strptime(schedule["schedule_departure_time"], "%H:%M")
    arr_time = datetime.strptime(schedule["schedule_arrival_time"], "%H:%M")
    schedule_duration = arr_time - dep_time
    if schedule_duration.total_seconds() < 0:
        schedule_duration += timedelta(days=1)
    
    route_duration_str = route.get("bus_trip_duration") if trip_type == "bus" else route.get("flight_duration")
    h, m, s = map(int, route_duration_str.split(":"))
    route_duration = timedelta(hours=h, minutes=m, seconds=s)
    
    if route_duration >= timedelta(hours=23, minutes=59):
        # для дуже довгих маршрутів беремо будь-який розклад
        return True

    # для коротких маршрутів — ±5 хв
    delta = timedelta(minutes=5)
    return abs(schedule_duration - route_duration) <= delta

# --- Функція генерації прив'язки сезону до розкладу ---
def generate_schedule_assignments(seasons, schedules, routes, trip_type="bus", avg_per_season=5):
    assignments = []
    for season in seasons:
        route_number = season["route_number"]
        season_start = season["season_start_date"]
        season_end = season["season_end_date"]
        route = routes[route_number]

        # відбираємо лише ті розклади, які підходять під duration маршруту
        matching_schedules = [s for s in schedules if is_schedule_matching_duration(s, route, trip_type)]
        if not matching_schedules:
            continue  # якщо нічого не підходить, пропускаємо

        selected_schedules = random.sample(matching_schedules, k=min(avg_per_season, len(matching_schedules)))

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

# --- Генерація ---
bus_assignments = generate_schedule_assignments(bus_seasons, bus_schedules, bus_routes, "bus")
flight_assignments = generate_schedule_assignments(flight_seasons, flight_schedules, flight_routes, "flight")

# --- Збереження ---
with open("out/season_schedules.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus trip season schedules": bus_assignments,
        "flight season schedules": flight_assignments
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_assignments)} автобусних та {len(flight_assignments)} авіаційних прив'язок сезону до розкладу")
