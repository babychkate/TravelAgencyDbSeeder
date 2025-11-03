import json
import random

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Завантаження туристичних сезонів ---
with open("in/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

    
# --- Завантаження типів харчувань ---
with open("in/classifiers.json", "r", encoding="utf-8") as f:
    meal_types = json.load(f)["meal types"]

meal_multipliers = {
    "Room Only (RO)": 1.0,
    "Bed & Breakfast (BB)": 1.25,
    "Half Board (HB)": 1.5,
    "Full Board (FB)": 1.75,
    "All Inclusive (AI)": 2.00
}

# --- Сезонні корекції ---
high_demand_seasons = ["Peak Holiday Season", "Hot Season"]
low_demand_seasons = ["Low Tourist Flow", "Shoulder Season"]

meal_price_seasons = []

for season in tourist_seasons:
    hotel_name = season["hotel_name"]
    season_name = season["additional_info_name"]
    start_date = season["tourist_season_start_date"]
    end_date = season["tourist_season_end_date"]

    # Знайти готель і його зірки
    hotel = next((h for h in hotels if h["hotel_name"] == hotel_name), None)
    stars = hotel.get("hotel_rate", 3) if hotel else 3

    # Базова ціна за зірками з ±10% варіацією
    if stars == 2:
        base_price = random.uniform(20, 40)
    elif stars == 3:
        base_price = random.uniform(40, 70)
    elif stars == 4:
        base_price = random.uniform(70, 150)
    else:
        base_price = random.uniform(150, 300)
    base_price *= random.uniform(0.9, 1.1)  # ±10% варіація

    # Сезонна корекція
    if season_name in high_demand_seasons:
        season_multiplier = 1.2  # +20%
    elif season_name in low_demand_seasons:
        season_multiplier = random.uniform(0.8, 0.9)  # -10–20%
    else:
        season_multiplier = 1.0  # без зміни

    # Генеруємо ціни для кожного типу харчування
    for meal in meal_types:
        meal_multiplier = meal_multipliers[meal] * random.uniform(0.9, 1.1)  # ±5–10%
        final_price = round(base_price * season_multiplier * meal_multiplier, 2)

        meal_price_seasons.append({
            "hotel_name": hotel_name,
            "tourist_season_start_date": start_date,
            "tourist_season_end_date": end_date,
            "meal_type_name": meal,
            "meal_price_per_person": final_price
        })

# --- Запис у JSON ---
with open("out/meal_price_seasons.json", "w", encoding="utf-8") as f:
    json.dump({"meal price seasons": meal_price_seasons}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(meal_price_seasons)} meal price season items")
