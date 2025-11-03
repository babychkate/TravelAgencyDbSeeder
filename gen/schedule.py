import json

# --- Зчитування днів ---
with open("in/schedule_days.json", "r", encoding="utf-8") as f:
    schedule_days = json.load(f)["schedule days"]

# --- Зчитування годин розкладу ---
with open("out/schedule_hours.json", "r", encoding="utf-8") as f:
    schedule_hours_data = json.load(f)
    bus_hours = schedule_hours_data.get("bus schedule hours", [])
    flight_hours = schedule_hours_data.get("flight schedule hours", [])

# --- Генерація повного розкладу для автобусів ---
bus_schedules = []
for day in schedule_days:
    day_name = day["schedule_day_name"]
    for hour in bus_hours:
        bus_schedules.append({
            "schedule_day_name": day_name,
            "schedule_departure_time": hour["schedule_departure_time"],
            "schedule_arrival_time": hour["schedule_arrival_time"]
        })

# --- Генерація повного розкладу для авіації ---
flight_schedules = []
for day in schedule_days:
    day_name = day["schedule_day_name"]
    for hour in flight_hours:
        flight_schedules.append({
            "schedule_day_name": day_name,
            "schedule_departure_time": hour["schedule_departure_time"],
            "schedule_arrival_time": hour["schedule_arrival_time"]
        })

# --- Збереження у JSON ---
with open("out/schedules.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus schedules": bus_schedules,
        "flight schedules": flight_schedules
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_schedules)} автобусних та {len(flight_schedules)} авіаційних записів для schedules")
