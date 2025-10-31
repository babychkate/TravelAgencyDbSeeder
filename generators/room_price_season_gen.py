import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування даних ---
with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open(base_path / "output/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

with open(base_path / "data/hotel_details.json", "r", encoding="utf-8") as f:
    hotel_details = json.load(f)

# --- Підготовка даних ---
hotel_room_types = hotel_details["hotel room types"]
hotel_room_type_beds = hotel_details["hotel room type beds"]

# Словник правил для цін
room_type_base_price = {
    "Single": 50,
    "Double": 80,
    "Deluxe": 120,
    "Family": 150,
    "Suite": 200
}

# --- Генерація room_price_season ---
room_price_season = []

for ts in tourist_seasons:
    hotel_name = ts["hotel_name"]
    season_start = ts["tourist_season_start_date"]
    season_end = ts["tourist_season_end_date"]
    
    for room_type in hotel_room_types:
        r_type_name = room_type["hotel_room_type_name"]
        max_adults = room_type["max_adults"]
        max_children = room_type["max_children"]
        
        # Беремо всі beds для цього типу кімнати
        beds_for_type = [
            b for b in hotel_room_type_beds
            if b["hotel_room_type_name"] == r_type_name
        ]
        
        for bed in beds_for_type:
            bed_name = bed["bed_type_name"]
            
            # Генеруємо ціну на людину
            base_price = room_type_base_price.get(r_type_name, 100)
            fluctuation = random.uniform(-0.2, 0.2)  # +/- 20%
            price_per_person = round(base_price * (1 + fluctuation), 2)
            
            room_price_season.append({
                "hotel_name": hotel_name,
                "tourist_season_start_date": season_start,
                "tourist_season_end_date": season_end,
                "hotel_room_type_name": r_type_name,
                "bed_type_name": bed_name,
                "max_adults": max_adults,
                "max_children": max_children,
                "room_price_per_person": price_per_person
            })

# --- Збереження ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "room_price_season.json", "w", encoding="utf-8") as f:
    json.dump({"room price seasons": room_price_season}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(room_price_season)} записів для room_price_season")
