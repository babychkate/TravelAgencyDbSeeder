import json
import random

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Завантаження nearby objects ---
with open("in/hotel_base.json", "r", encoding="utf-8") as f:
    nearby_objects = json.load(f)["nearby objects"]

hotel_nearby_objects = []

# --- Швидкості для розрахунку часу ---
WALK_SPEED_KMH = 3
TRANSPORT_SPEED_KMH = 30

# --- Встановлюємо відстані залежно від типу об'єкта ---
distance_ranges = {
    "Airport": (5, 40),
    "Museum": (0.3, 10),
    "Restaurant": (0.3, 5),
    "Cafe": (0.2, 5),
    "Park": (0.3, 7),
    "Beach": (0.5, 20),
    "Hotel": (0.5, 10),
    "Hospital": (1, 15),
    "Theater": (0.3, 7),
    "Historical Site": (0.3, 5),
}

# --- Генеруємо 500 записів ---
for _ in range(500):
    hotel = random.choice(hotels)
    hotel_name = hotel["hotel_name"]
    city = hotel.get("city_name", "")

    city_objects = [obj for obj in nearby_objects if city in obj["nearby_object_address"]]
    if not city_objects:
        city_objects = nearby_objects

    obj = random.choice(city_objects)
    obj_type = obj["nearby_object_type_name"]

    distance_min, distance_max = distance_ranges.get(obj_type, (0.5, 10))
    distance = round(random.uniform(distance_min, distance_max), 2)

    time_by_walk = round(distance / WALK_SPEED_KMH * 60)
    time_by_transport = round(distance / TRANSPORT_SPEED_KMH * 60)

    hotel_nearby_objects.append({
        "hotel_name": hotel_name,
        "nearby_object_name": obj["nearby_object_name"],
        "from_hotel_to_object_distance_km": distance,
        "time_to_object_by_transport_min": time_by_transport,
        "time_to_object_by_walk_min": time_by_walk
    })

# --- Запис у JSON ---
with open("out/hotel_nearby_objects.json", "w", encoding="utf-8") as f:
    json.dump({"hotel nearby objects": hotel_nearby_objects}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(hotel_nearby_objects)} hotel nearby object links.")
