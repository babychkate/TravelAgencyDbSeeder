import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# --- 1. Налаштування ---
base_path = Path(__file__).parent.parent

# --- 2. Зчитування даних ---
with open(base_path / "data/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open(base_path / "data/classifiers.json", "r", encoding="utf-8") as f:
    additional_infos = json.load(f)["additional infos"]

# --- 3. Базові періоди ---
base_periods = [
    ("2025-12-01", "2026-01-15"),
    ("2026-01-16", "2026-02-28")
]

# --- 4. Функція для випадкового зсуву дат ---
def random_shift_date(date_str, shift_range=(-5, 5)):
    """Додає випадковий зсув до дати (у днях)"""
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    shift_days = random.randint(*shift_range)
    shifted_date = base_date + timedelta(days=shift_days)
    return shifted_date.strftime("%Y-%m-%d")

# --- 5. Генерація сезонів ---
tourist_seasons = []

for hotel in hotels:
    hotel_name = hotel["hotel_name"]

    for start_date, end_date in base_periods:
        # зсув дат на випадкову кількість днів
        shifted_start = random_shift_date(start_date)
        shifted_end = random_shift_date(end_date)

        # гарантуємо, що кінець після початку
        if shifted_end < shifted_start:
            shifted_end = (datetime.strptime(shifted_start, "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")

        info = random.choice(additional_infos)["additional_info_name"]

        tourist_seasons.append({
            "tourist_season_start_date": shifted_start,
            "tourist_season_end_date": shifted_end,
            "hotel_name": hotel_name,
            "additional_info_name": info,
        })

# --- 6. Збереження результату ---
output_path = base_path / "output"
output_path.mkdir(exist_ok=True)

with open(output_path / "tourist_seasons.json", "w", encoding="utf-8") as f:
    json.dump({"tourist seasons": tourist_seasons}, f, ensure_ascii=False, indent=2)

print(f"✅ Згенеровано {len(tourist_seasons)} туристичних сезонів для {len(hotels)} готелів.")
