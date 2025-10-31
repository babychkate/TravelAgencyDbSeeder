import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Параметри ---
bus_prices = [80, 100, 120, 140, 160]
flight_prices = [150, 200, 250, 300, 350]

# --- Зчитування проміжних таблиць ---
with open(base_path / "output/bus_trip_season_schedule.json", "r", encoding="utf-8") as f:
    bus_season_schedules = json.load(f)["bus trip season schedules"]

with open(base_path / "output/flight_season_schedule.json", "r", encoding="utf-8") as f:
    flight_season_schedules = json.load(f)["flight season schedules"]

# --- Функція для створення конкретних поїздок ---
def generate_trips(season_schedules, trip_type="bus"):
    trips = []
    for s in season_schedules:
        start_date = datetime.strptime(s[f"{trip_type}_trip_season_start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(s[f"{trip_type}_trip_season_end_date"], "%Y-%m-%d")
        day_name = s["day_name"]

        # Додаємо ще пів місяця (15 днів) до кінця сезону
        extended_end_date = end_date + timedelta(days=15)

        current_date = start_date
        while current_date <= extended_end_date :
            if current_date.strftime("%A") == day_name:
                trips.append({
                    "route_number": s["route_number"],
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    f"{trip_type}_trip_expected_price": random.choice(bus_prices if trip_type=="bus" else flight_prices),
                    f"{trip_type}_trip_departure_time": s["schedule_departure_time"],
                    f"{trip_type}_trip_arrival_time": s["schedule_arrival_time"]
                })
            current_date += timedelta(days=1)
    return trips

# --- Генерація ---
bus_trips = generate_trips(bus_season_schedules, "bus")
flight_trips = generate_trips(flight_season_schedules, "flight")

# --- Збереження ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "bus_trip.json", "w", encoding="utf-8") as f:
    json.dump({"bus trips": bus_trips}, f, ensure_ascii=False, indent=2)

with open(output_path / "flight.json", "w", encoding="utf-8") as f:
    json.dump({"flights": flight_trips}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_trips)} автобусних поїздок")
print(f"Згенеровано {len(flight_trips)} авіарейсів")
