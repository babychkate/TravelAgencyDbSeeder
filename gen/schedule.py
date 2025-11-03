import json

# --- Зчитування днів ---
with open("in/schedule_days.json", "r", encoding="utf-8") as f:
    schedule_days = json.load(f)["schedule days"]

# --- Зчитування годин ---
with open("in/schedule_hours.json", "r", encoding="utf-8") as f:
    schedule_hours = json.load(f)["schedule hours"]

# --- Генеруємо комбінований розклад ---
schedules = []

for day in schedule_days:
    day_name = day["schedule_day_name"]
    for hour in schedule_hours:
        schedules.append({
            "schedule_day_name": day_name,
            "schedule_departure_time": hour["schedule_departure_time"],
            "schedule_arrival_time": hour["schedule_arrival_time"]
        })

# --- Запис у JSON ---
with open("out/schedules.json", "w", encoding="utf-8") as f:
    json.dump({"schedules": schedules}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(schedules)} записів для schedules")
