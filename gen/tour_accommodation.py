import json
import random

# --- Завантаження даних ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open("in/tourist_seasons.json", "r", encoding="utf-8") as f:
    tourist_seasons = json.load(f)["tourist seasons"]

with open("in/meal_price_seasons.json", "r", encoding="utf-8") as f:
    meal_price_seasons = json.load(f)["meal price seasons"]

with open("in/room_price_seasons.json", "r", encoding="utf-8") as f:
    room_price_seasons = json.load(f)["room price seasons"]

# --- Підготовка словників для швидкого доступу ---
meal_price_dict = {
    (item["hotel_name"], item["tourist_season_start_date"], item["tourist_season_end_date"], item["meal_type_name"]): item["meal_price_per_person"]
    for item in meal_price_seasons
}

room_price_dict = {
    (item["hotel_name"], item["tourist_season_start_date"], item["tourist_season_end_date"],
     item["hotel_room_type_name"], item["bed_type_name"]): item["room_price_per_person"]
    for item in room_price_seasons
}

# --- Генерація tour accommodations ---
tour_accommodations = []

for season in tourist_seasons:
    hotel_name = season["hotel_name"]
    season_start = season["tourist_season_start_date"]
    season_end = season["tourist_season_end_date"]
    
    # Вибираємо кімнати, які є для цього готелю і сезону
    room_types_in_season = [
        r for r in room_price_seasons 
        if r["hotel_name"] == hotel_name
        and r["tourist_season_start_date"] == season_start
        and r["tourist_season_end_date"] == season_end
    ]
    
    # Унікальні комбінації кімната+ліжко
    room_types_set = set(
        (r["hotel_room_type_name"], r["bed_type_name"], r["max_adults"], r["max_children"])
        for r in room_types_in_season
    )
    
    for room_type_name, bed_name, max_adults, max_children in room_types_set:
        # Вибір типів харчування для цієї кімнати (1-2 типи)
        possible_meals = [
            m for m in meal_price_seasons
            if m["hotel_name"] == hotel_name
            and m["tourist_season_start_date"] == season_start
            and m["tourist_season_end_date"] == season_end
        ]
        meals_for_room = random.sample(possible_meals, k=min(len(possible_meals), random.randint(1, 2)))
        
        for meal in meals_for_room:
            meal_name = meal["meal_type_name"]
            meal_price = meal_price_dict[(hotel_name, season_start, season_end, meal_name)]
            room_price = room_price_dict[(hotel_name, season_start, season_end, room_type_name, bed_name)]
            
            total_price_per_person = round(room_price + meal_price, 2)
            
            tour_accommodations.append({
                "hotel_name": hotel_name,
                "tourist_season_start_date": season_start,
                "tourist_season_end_date": season_end,
                "hotel_room_type_name": room_type_name,
                "bed_type_name": bed_name,
                "max_adults": max_adults,
                "max_children": max_children,
                "meal_type_name": meal_name,
                "total_price_per_person": total_price_per_person
            })

# --- Збереження у JSON ---
with open("out/tour_accommodations.json", "w", encoding="utf-8") as f:
    json.dump({"tour accommodations": tour_accommodations}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(tour_accommodations)} записів для tour accommodations")
