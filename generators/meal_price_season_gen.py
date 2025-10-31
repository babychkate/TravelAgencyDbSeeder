import json
import random
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Зчитування даних ---
with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open(base_path / "output/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

with open(base_path / "data/classifiers.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)

meal_types = classifiers.get("meal types", [])
if not meal_types:
    {"meal_type_name": "Room Only (RO)"},
    {"meal_type_name": "Bed & Breakfast (BB)"},
    {"meal_type_name": "Half Board (HB)"},
    {"meal_type_name": "Full Board (FB)"},
    {"meal_type_name": "All Inclusive (AI)"}

# --- Словник базових цін ---
meal_type_base_price = {
    "Room Only (RO)": 10,
    "Bed & Breakfast (BB)": 25,
    "Half Board (HB)": 45,
    "Full Board (FB)": 75,
    "All Inclusive (AI)": 100
}

# --- Генерація meal_price_season ---
meal_price_season = []

for ts in tourist_seasons:
    hotel_name = ts["hotel_name"]
    season_start = ts["tourist_season_start_date"]
    season_end = ts["tourist_season_end_date"]
    
    for meal in meal_types:
        meal_name = meal["meal_type_name"]
        base_price = meal_type_base_price[meal_name]
        fluctuation = random.uniform(-0.10, 0.10)  # +/- 10%
        meal_price_per_person = round(base_price * (1 + fluctuation), 2)
        
        meal_price_season.append({
            "hotel_name": hotel_name,
            "tourist_season_start_date": season_start,
            "tourist_season_end_date": season_end,
            "meal_type_name": meal_name,
            "meal_price_per_person": meal_price_per_person
        })

# --- Збереження ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "meal_price_season.json", "w", encoding="utf-8") as f:
    json.dump({"meal price seasons": meal_price_season}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(meal_price_season)} записів для meal_price_season")