import json
import random
from datetime import datetime, timedelta

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Класифікатор сезонів ---
with open("in/classifiers.json", "r", encoding="utf-8") as f:
    all_seasons = json.load(f)["seasons"]

# --- Відповідність місяців ---
month_to_season_type = {
    12: ["Winter Season", "Festival Period", "Peak Holiday Season", "Low Tourist Flow"],
    1: ["Winter Season", "Festival Period", "Low Tourist Flow"],
    2: ["Winter Season", "Low Tourist Flow"],
    3: ["Shoulder Season", "Low Tourist Flow"],
    4: ["Shoulder Season", "Low Tourist Flow", "Rainy Season"],
    5: ["Shoulder Season", "Peak Holiday Season"],
    6: ["Summer Season", "Hot Season", "Peak Holiday Season"],
    7: ["Summer Season", "Hot Season", "Peak Holiday Season"],
    8: ["Summer Season", "Hot Season", "Peak Holiday Season"],
    9: ["Shoulder Season", "Low Tourist Flow", "Rainy Season"],
    10: ["Shoulder Season", "Low Tourist Flow", "Rainy Season"],
    11: ["Low Tourist Flow", "Rainy Season"]
}

tourist_seasons = []
target_total = 200  # 🎯 загальна кількість записів
current_total = 0

# --- Генерація сезонів ---
while current_total < target_total:
    hotel = random.choice(hotels)
    hotel_name = hotel["hotel_name"]
    current_date = datetime(2025, random.randint(1, 10), random.randint(1, 25))

    season_length_months = random.randint(1, 2)
    end_month = current_date.month + season_length_months - 1
    end_year = current_date.year
    if end_month > 12:
        end_month -= 12
        end_year += 1

    end_date = datetime(end_year, end_month, 28)

    # Логічний вибір сезону по місяцю
    possible_seasons = month_to_season_type.get(current_date.month, all_seasons)
    season_name = random.choice(possible_seasons)

    tourist_seasons.append({
        "hotel_name": hotel_name,
        "tourist_season_start_date": current_date.strftime("%Y-%m-%d"),
        "tourist_season_end_date": end_date.strftime("%Y-%m-%d"),
        "additional_info_name": season_name
    })

    current_total += 1

# --- Запис ---
with open("out/tourist_seasons.json", "w", encoding="utf-8") as f:
    json.dump({"tourist seasons": tourist_seasons}, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(tourist_seasons)} tourist season entries.")
