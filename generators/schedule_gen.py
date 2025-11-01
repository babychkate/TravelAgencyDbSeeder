import json
from pathlib import Path

# --- Базовий шлях ---
base_path = Path(__file__).parent.parent

# --- Зчитування даних ---
with open(base_path / "data/schedules.json", "r", encoding="utf-8") as f:
    data = json.load(f)

schedule_hours = data.get("schedule_hours", [])
schedule_days = data.get("schedule_day", [])

# --- Підготовка всіх комбінацій ---
all_schedules = []
for day in schedule_days:
    for hour in schedule_hours:
        all_schedules.append({
            "schedule_day_name": day["schedule_day_name"],
            "schedule_arrival_time": hour["schedule_arrival_time"],
            "schedule_departure_time": hour["schedule_departure_time"]
        })

# --- Збереження у JSON ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "schedules.json", "w", encoding="utf-8") as f:
    json.dump({"schedule_combinations": all_schedules}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(all_schedules)} комбінацій розкладу")
