import json
import random
from collections import defaultdict

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Завантаження фасіліті ---
with open("in/hotel_base.json", "r", encoding="utf-8") as f:
    base_facilities = json.load(f)["facilities"]

hotel_facilities = []

# --- Категорії і ймовірності для малих/великих готелів ---
category_weights = {
    "General": 1.0,
    "Food & Drink": 0.8,
    "Wellness": 0.5,
    "Pools": 0.6,
    "Sports": 0.3,
    "Business": 0.4,
    "Family": 0.5,
    "Accessibility": 0.3,
    "Parking & Transport": 0.7,
    "Recreation": 0.4
}

# --- Групування фасіліті за категоріями ---
facilities_by_category = defaultdict(list)
for f in base_facilities:
    facilities_by_category[f["category_of_facility_name"]].append(f["facility_name"])

# --- Генерація послуг ---
for hotel in hotels:
    hotel_rate = hotel.get("hotel_rate", 3)
    room_count = hotel.get("hotel_room_count", 50)

    # Визначаємо бажану кількість послуг на готель
    num_services = max(5, min(10, int(random.gauss(7.5, 1.5))))

    selected_services = []
    used_categories = set()

    # Поки не набрали потрібну кількість унікальних категорій
    while len(selected_services) < num_services:
        # Випадкова категорія
        category = random.choices(list(category_weights.keys()), weights=list(category_weights.values()))[0]

        # Уникаємо повторів категорій, якщо є альтернативи
        if category in used_categories and len(used_categories) < len(category_weights):
            continue

        # Випадкова послуга з цієї категорії
        if facilities_by_category[category]:
            facility_name = random.choice(facilities_by_category[category])

            # Визначаємо платність
            paid_categories = ["Wellness", "Pools", "Business", "Sports", "Recreation", "Family"]
            is_paid = 1 if category in paid_categories and random.random() < 0.8 else 0

            selected_services.append({
                "hotel_name": hotel["hotel_name"],
                "facility_name": facility_name,
                "hotel_facility_is_paid": is_paid
            })
            used_categories.add(category)

    hotel_facilities.extend(selected_services)

# --- Підганяємо кількість записів до 1500 ---
current_count = len(hotel_facilities)
if current_count < 1500:
    additional_needed = 1500 - current_count
    hotel_facilities.extend(random.choices(hotel_facilities, k=additional_needed))
elif current_count > 1500:
    hotel_facilities = random.sample(hotel_facilities, 1500)

# --- Запис у JSON ---
with open("out/hotel_facilities.json", "w", encoding="utf-8") as f:
    json.dump({"hotel facilities": hotel_facilities}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(hotel_facilities)} hotel facilities with diverse categories per hotel.")
