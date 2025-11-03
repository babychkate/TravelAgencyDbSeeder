import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Параметри ---
bus_prices = [80, 100, 120, 140, 160]
bus_weights = [0.1, 0.2, 0.4, 0.2, 0.1]

flight_prices = [150, 200, 250, 300, 350]
flight_weights = [0.1, 0.2, 0.4, 0.2, 0.1]

# --- Зчитування сезонного розкладу ---
with open(base_path / "out/season_schedules.json", "r", encoding="utf-8") as f:
    season_schedules_data = json.load(f)
    bus_season_schedules = season_schedules_data.get("bus trip season schedules", [])
    flight_season_schedules = season_schedules_data.get("flight season schedules", [])

# --- Функція генерації trips ---
def generate_trips(season_schedules, trip_type="bus"):
    trips = []
    prices = bus_prices if trip_type == "bus" else flight_prices
    weights = bus_weights if trip_type == "bus" else flight_weights

    for s in season_schedules:
        start_date = datetime.strptime(s["season_start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(s["season_end_date"], "%Y-%m-%d")
        day_name = s["schedule_day_name"]

        current_date = start_date
        while current_date <= end_date:
            if current_date.strftime("%A") == day_name:
                trips.append({
                    "route_number": s["route_number"],
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    f"{trip_type}_trip_expected_price": random.choices(prices, weights=weights)[0],
                    f"{trip_type}_trip_departure_time": s["schedule_departure_time"],
                    f"{trip_type}_trip_arrival_time": s["schedule_arrival_time"]
                })
            current_date += timedelta(days=1)
    return trips

# --- Генерація ---
bus_trips = generate_trips(bus_season_schedules, "bus")
flight_trips = generate_trips(flight_season_schedules, "flight")

# --- Збереження ---
output_path = base_path / "out"
output_path.mkdir(exist_ok=True)

with open(output_path / "bus_trip.json", "w", encoding="utf-8") as f:
    json.dump({"bus trips": bus_trips}, f, ensure_ascii=False, indent=2)

with open(output_path / "flight.json", "w", encoding="utf-8") as f:
    json.dump({"flights": flight_trips}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_trips)} автобусних поїздок")
print(f"Згенеровано {len(flight_trips)} авіарейсів")
