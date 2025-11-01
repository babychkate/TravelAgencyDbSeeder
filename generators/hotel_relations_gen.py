import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

with open(base_path / "sources/hotel_base_source.json", "r", encoding="utf-8") as f:
    hotel_base = json.load(f)

with open(base_path / "data/hotel_details.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)

facilities = hotel_base["facilities"]
nearby_objects = hotel_base["nearby objects"]
pricing_policies = classifiers["pricing policies"]

hotels = hotels["hotels"]  # беремо список готелів

# --- Генерація зв'язків ---
hotel_facilities_links = []
hotel_nearby_objects_links = []
hotel_pricing_policies_links = []

for hotel in hotels:
    hotel_name = hotel["hotel_name"]

    # 15 випадкових зручностей на готель
    hotel_facilities_links.extend([
        {
            "hotel_name": hotel_name,
            "facility_name": f["facility_name"],
            "hotel_facility_is_paid": random.choice([0, 1]) 
        }
        for f in random.sample(facilities, min(15, len(facilities)))
    ])

    # 5 випадкових об'єктів поруч
    hotel_nearby_objects_links.extend([
        {
            "hotel_name": hotel_name, 
            "nearby_object_name": obj["nearby_object_name"],
            "from_hotel_to_object_distance_km": round(random.uniform(0.1, 10.0), 2),
            "time_to_object_by_transport_min": random.randint(2, 30),
            "time_to_object_by_walk_min": random.randint(5, 60)
        }
        for obj in random.sample(nearby_objects, min(5, len(nearby_objects)))
    ])

    # 2 випадкові політики ціноутворення
    hotel_pricing_policies_links.extend([
        {"hotel_name": hotel_name, "policy_name": p["policy_type_name"]}
        for p in random.sample(pricing_policies, min(2, len(pricing_policies)))
    ])

# --- Збереження у файли для подальшої роботи ---
hotel_relations = {
    "hotel facilities": hotel_facilities_links,
    "hotel nearby objects": hotel_nearby_objects_links,
    "hotel pricing policies": hotel_pricing_policies_links
}

# Вивід кількості елементів
print(f"Створено зв'язків готель → зручності: {len(hotel_facilities_links)}")
print(f"Створено зв'язків готель → об'єкти поруч: {len(hotel_nearby_objects_links)}")
print(f"Створено зв'язків готель → політики ціноутворення: {len(hotel_pricing_policies_links)}")

with open(base_path / "data/hotel_relations.json", "w", encoding="utf-8") as f:
    json.dump(hotel_relations, f, ensure_ascii=False, indent=2)

print("Генерація зв'язків завершена! Дані збережено в 'hotel_relations.json'")
