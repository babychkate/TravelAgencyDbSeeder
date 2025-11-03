import json
import random
from datetime import datetime, timedelta

# --- Читаємо маршрути ---
with open("out/routes.json", "r", encoding="utf-8") as f:
    routes_data = json.load(f)
    bus_routes = routes_data.get("bus trip routes", [])
    flight_routes = routes_data.get("flight routes", [])

# --- Читаємо готелі ---
with open("out/tour_accommodations.json", "r", encoding="utf-8") as f:
    accommodations = json.load(f)["tour accommodations"]

# --- Функція генерації сезону під готельний період ---
def generate_seasons_for_route(route_number, city_name):
    # шукаємо готельні сезони для міста прибуття
    city_seasons = [
        (datetime.strptime(acc["tourist_season_start_date"], "%Y-%m-%d"),
         datetime.strptime(acc["tourist_season_end_date"], "%Y-%m-%d"))
        for acc in accommodations
        if acc["hotel_name"].lower().find(city_name.lower()) != -1
    ]
    
    seasons = []
    # якщо є готельні сезони — беремо два випадкових періоди всередині
    if city_seasons:
        for _ in range(2):
            start, end = random.choice(city_seasons)
            season_length = random.randint(28, 32)  # ~1 місяць
            if (end - start).days > season_length:
                season_start = start + timedelta(days=random.randint(0, (end-start).days-season_length))
                season_end = season_start + timedelta(days=season_length)
            else:
                season_start, season_end = start, end
            seasons.append({
                "route_number": route_number,
                "season_start_date": season_start.strftime("%Y-%m-%d"),
                "season_end_date": season_end.strftime("%Y-%m-%d"),
            })
    else:
        # якщо немає готельного сезону — просто рандом в межах року
        year_start = datetime(2025, 11, 15)
        for _ in range(2):
            season_start = year_start + timedelta(days=random.randint(0, 365-30))
            season_end = season_start + timedelta(days=random.randint(28, 32))
            seasons.append({
                "route_number": route_number,
                "season_start_date": season_start.strftime("%Y-%m-%d"),
                "season_end_date": season_end.strftime("%Y-%m-%d")
            })
    return seasons

# --- Генерація всіх сезонів окремо для автобусів і літаків ---
bus_seasons = []
flight_seasons = []

for route in bus_routes:
    city_name = route["arrival_bus_station_name"]
    bus_seasons.extend(generate_seasons_for_route(route["route_number"], city_name))

for route in flight_routes:
    city_name = route["arrival_airport_name"]
    flight_seasons.extend(generate_seasons_for_route(route["route_number"], city_name))

# --- Збереження ---
with open("out/seasons.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus seasons": bus_seasons,
        "flight seasons": flight_seasons
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_seasons)} автобусних та {len(flight_seasons)} авіаційних сезонів.")
