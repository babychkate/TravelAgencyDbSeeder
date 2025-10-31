import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування даних ---
with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open(base_path / "data/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

with open(base_path / "data/classifiers.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

with open(base_path / "data/room_price_season.json", "r", encoding="utf-8") as f:
    room_price_seasons = json.load(f)["room price seasons"]

with open(base_path / "data/meal_price_season.json", "r", encoding="utf-8") as f:
    meal_price_seasons = json.load(f)["meal price seasons"]

# --- Підготовка типів харчування ---
meal_types = [m["meal_type_name"] for m in classifiers.get("meal types", [])]
if not meal_types:
    meal_types = ["Room Only (RO)", "Bed & Breakfast (BB)", "Half Board (HB)", "Full Board (FB)", "All Inclusive (AI)"]

# --- Генерація tour_accommodation ---
tour_accommodation = []
success_rate = 0.2  # 20%

for ts in tourist_seasons:
    hotel_name = ts["hotel_name"]
    season_start = ts["tourist_season_start_date"]
    season_end = ts["tourist_season_end_date"]
    
    rooms_for_hotel = [
        r for r in room_price_seasons 
        if r["hotel_name"] == hotel_name and
           r["tourist_season_start_date"] == season_start and
           r["tourist_season_end_date"] == season_end
    ]
    
    for room in rooms_for_hotel:
        room_type_name = room["hotel_room_type_name"]
        max_adults = room["max_adults"]
        max_children = room["max_children"]
        
        for meal_type in meal_types:
            if random.random() < success_rate:
                tour_accommodation.append({
                    "hotel_name": hotel_name,
                    "tourist_season_start_date": season_start,
                    "tourist_season_end_date": season_end,
                    "hotel_room_type_name": room_type_name,
                    "max_adults": max_adults,
                    "max_children": max_children,
                    "meal_type_name": meal_type
                })

# --- Збереження ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "tour_accommodation.json", "w", encoding="utf-8") as f:
    json.dump({"tour accommodations": tour_accommodation}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(tour_accommodation)} записів tour_accommodation")
