import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування згенерованих авіарейсів ---
with open(base_path / "output/flight_route.json", "r", encoding="utf-8") as f:
    flight_routes = json.load(f)["flight_route"]

# --- Параметри генерації ---
num_seasons_per_route = 2
season_length_days = [30, 45, 60]  # тривалість сезону

# --- Генерація сезонів ---
flight_seasons = []

for route in flight_routes:
    route_number = route["flight_number"]
    current_date = datetime(2025, 12, 1)  # стартуємо з грудня 2025
    
    for _ in range(num_seasons_per_route):
        length = random.choice(season_length_days)
        end_date = current_date + timedelta(days=length)
        
        flight_seasons.append({
            "route_number": route_number,
            "flight_trip_season_start_date": current_date.strftime("%Y-%m-%d"),
            "flight_trip_season_end_date": end_date.strftime("%Y-%m-%d")
        })
        
        # Наступний сезон починається після попереднього
        current_date = end_date + timedelta(days=1)

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "flight_season.json", "w", encoding="utf-8") as f:
    json.dump({"flight seasons": flight_seasons}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(flight_seasons)} авіаційних сезонів")
