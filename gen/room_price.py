import json
import random

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Завантаження туристичних сезонів ---
with open("in/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

# --- Завантаження деталей кімнат ---
with open("in/hotel_details.json", "r", encoding="utf-8") as f:
    hotel_details = json.load(f)

hotel_room_types = hotel_details["hotel room types"]
hotel_room_type_beds = hotel_details["hotel room type beds"]

# --- Базові ціни по типах кімнат ---
room_type_base_price = {
    "Single": 200,
    "Double": 370,
    "Deluxe": 500,
    "Family": 600,
    "Suite": 700
}

# --- Сезонні корекції ---
high_demand_seasons = ["Peak Holiday Season", "Hot Season"]
low_demand_seasons = ["Low Tourist Flow", "Shoulder Season"]

room_price_seasons = []

for season in tourist_seasons:
    hotel_name = season["hotel_name"]
    season_name = season["additional_info_name"]
    start_date = season["tourist_season_start_date"]
    end_date = season["tourist_season_end_date"]

    # Сезонний множник
    if season_name in high_demand_seasons:
        season_multiplier = 1.2
    elif season_name in low_demand_seasons:
        season_multiplier = random.uniform(0.7, 0.9)
    else:
        season_multiplier = 1.0

    for room_type in hotel_room_types:
        r_type_name = room_type["hotel_room_type_name"]
        max_adults = room_type["max_adults"]
        max_children = room_type["max_children"]

        # Всі beds для цього типу кімнати
        beds_for_type = [b for b in hotel_room_type_beds if b["hotel_room_type_name"] == r_type_name]

        for bed in beds_for_type:
            bed_name = bed["bed_type_name"]

            # Базова ціна + сезон + невелика флуктуація
            base_price = room_type_base_price.get(r_type_name, 100)
            base_price *= season_multiplier
            price_per_person = round(base_price * random.uniform(0.95, 1.05), 2)  # ±5% по bed

            room_price_seasons.append({
                "hotel_name": hotel_name,
                "tourist_season_start_date": start_date,
                "tourist_season_end_date": end_date,
                "hotel_room_type_name": r_type_name,
                "bed_type_name": bed_name,
                "max_adults": max_adults,
                "max_children": max_children,
                "room_price_per_person": price_per_person
            })

# --- Запис у JSON ---
with open("out/room_price_seasons.json", "w", encoding="utf-8") as f:
    json.dump({"room price seasons": room_price_seasons}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(room_price_seasons)} room price season items")
