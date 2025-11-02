import json
import random
from pathlib import Path

# --- Базовий шлях ---
base_path = Path(__file__).parent.parent

# --- Зчитування джерел ---
with open(base_path / "sources/hotel_base_source.json", "r", encoding="utf-8") as f:
    hotel_base = json.load(f)

with open(base_path / "data/hotel_details.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)

facilities = hotel_base["facilities"]
nearby_objects = hotel_base["nearby objects"]
pricing_policies = classifiers["pricing policies"]
hotels = hotels["hotels"]  # список готелів

# --- Результуючі списки ---
hotel_facilities_links = []
hotel_nearby_objects_links = []
hotel_pricing_policies_links = []

# --- Набір платних зручностей ---
paid_facilities = {"Daily Housekeeping", "Bar", "Spa & Sauna", "Massage Services", "Baby Sitting Service"}

# --- Генерація зв’язків ---
for hotel in hotels:
    hotel_name = hotel["hotel_name"]
    stars = hotel.get("hotel_stars", random.randint(2, 5))
    city = hotel.get("hotel_city", "Kyiv")
    avg_price = hotel.get("avg_price_per_night_usd", random.randint(50, 250))

    # ------------------------ #
    # 1️⃣ ЗРУЧНОСТІ Готелю
    # ------------------------ #
    num_facilities = random.randint(5 + stars, 10 + stars * 2)
    selected_facilities = random.sample(facilities, min(num_facilities, len(facilities)))

    for f in selected_facilities:
        facility_name = f["facility_name"]
        hotel_facilities_links.append({
            "hotel_name": hotel_name,
            "facility_name": facility_name,
            "hotel_facility_is_paid": 1 if facility_name in paid_facilities else 0
        })

    # ------------------------ #
    # 2️⃣ ОБ’ЄКТИ ПОБЛИЗУ
    # ------------------------ #
    # відбираємо ті, що збігаються з містом готелю (якщо є)
    city_objects = [obj for obj in nearby_objects if obj.get("city") == city]
    if city_objects:
        chosen_objects = random.sample(city_objects, min(5, len(city_objects)))
    else:
        chosen_objects = random.sample(nearby_objects, min(5, len(nearby_objects)))

    for obj in chosen_objects:
        distance = round(random.uniform(0.3, 8.0), 2)
        walk_min = int(distance * random.uniform(10, 14))  # 10–14 хв/км
        transport_min = max(2, int(distance * random.uniform(2, 4)))  # 2–4 хв/км

        # якщо у назві готелю є “Center” або “Downtown” — відстані коротші
        if any(keyword in hotel_name for keyword in ["Center", "Downtown"]):
            distance = round(random.uniform(0.2, 3.0), 2)
            walk_min = int(distance * random.uniform(8, 12))
            transport_min = max(1, int(distance * random.uniform(1.5, 3)))

        hotel_nearby_objects_links.append({
            "hotel_name": hotel_name,
            "nearby_object_name": obj["nearby_object_name"],
            "from_hotel_to_object_distance_km": distance,
            "time_to_object_by_transport_min": transport_min,
            "time_to_object_by_walk_min": walk_min
        })

    # ------------------------ #
    # 3️⃣ ПОЛІТИКИ ЦІНОУТВОРЕННЯ
    # ------------------------ #
    # дорожчі готелі мають більше політик (наприклад, "Early Booking", "Flexible")
    if avg_price > 180:
        num_policies = 3
    elif avg_price > 100:
        num_policies = 2
    else:
        num_policies = 1

    chosen_policies = random.sample(pricing_policies, min(num_policies, len(pricing_policies)))
    for p in chosen_policies:
        hotel_pricing_policies_links.append({
            "hotel_name": hotel_name,
            "policy_name": p["policy_type_name"]
        })

# --- Збереження результатів ---
hotel_relations = {
    "hotel facilities": hotel_facilities_links,
    "hotel nearby objects": hotel_nearby_objects_links,
    "hotel pricing policies": hotel_pricing_policies_links
}

with open(base_path / "output/hotel_relations.json", "w", encoding="utf-8") as f:
    json.dump(hotel_relations, f, ensure_ascii=False, indent=2)

# --- Статистика ---
print(f"🏨 Згенеровано зв’язків готель → зручності: {len(hotel_facilities_links)}")
print(f"📍 Згенеровано зв’язків готель → об’єкти поруч: {len(hotel_nearby_objects_links)}")
print(f"💰 Згенеровано зв’язків готель → політики ціноутворення: {len(hotel_pricing_policies_links)}")
print("✅ Генерація завершена! Дані збережено в 'hotel_relations.json'")
