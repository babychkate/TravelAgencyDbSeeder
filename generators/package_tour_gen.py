import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування даних ---
with open(base_path / "output/tour_accommodation.json", "r", encoding="utf-8") as f:
    tour_accommodations = json.load(f)["tour accommodations"]

with open(base_path / "data/organizations.json", "r", encoding="utf-8") as f:
    organizations = json.load(f)

with open(base_path / "data/classifiers.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

# --- Статуси турів ---
package_tour_statuses = [s["package_tour_status_name"] for s in classifiers.get("package tour statuses", [])]
if not package_tour_statuses:
    package_tour_statuses = ["Active", "Cancelled", "Draft"]

# --- Туроператори ---
tour_operators = [op["tour_operator_name"] for op in organizations.get("tour operators", [])]
if not tour_operators:
    tour_operators = [f"Tour Operator {i+1}" for i in range(10)]

# --- Генерація пакетних турів ---
num_package_tours = 6000
package_tours = []

for i in range(1, num_package_tours + 1):
    if not tour_accommodations:
        break  # немає доступного проживання

    tour_operator = random.choice(tour_operators)
    accommodation = random.choice(tour_accommodations)

    start_date = datetime.strptime(accommodation["tourist_season_start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(accommodation["tourist_season_end_date"], "%Y-%m-%d")

    available_days = (end_date - start_date).days
    if available_days < 3:
        continue  # пропускаємо дуже короткі сезони

    tour_length = random.randint(3, min(10, available_days))
    package_start_date = start_date + timedelta(days=random.randint(0, available_days - tour_length))
    package_end_date = package_start_date + timedelta(days=tour_length)

    package_tours.append({
        "tour_operator_name": tour_operator,
        "tour_accommodation": accommodation,  # тільки реально згенеровані
        "package_tour_status_name": random.choice(package_tour_statuses),
        "package_tour_name": f"Tour {i:04d}",
        "package_tour_description": f"Description for Tour {i:04d}",
        "package_tour_start_date": package_start_date.strftime("%Y-%m-%d"),
        "package_tour_end_date": package_end_date.strftime("%Y-%m-%d"),
        "package_tour_max_tourists_count": random.randint(10, 50)
    })

# --- Збереження ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "package_tour.json", "w", encoding="utf-8") as f:
    json.dump({"package_tours": package_tours}, f, ensure_ascii=False, indent=2)

print(f"✅ Згенеровано {len(package_tours)} пакетних турів")
