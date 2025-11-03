import json
import random

# --- Завантаження готелів ---
with open("in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

# --- Завантаження політик ---
with open("in/hotel_details.json", "r", encoding="utf-8") as f:
    pricing_policies = json.load(f)["pricing policies"]

hotel_pricing_policies = []

# --- Ймовірності для кількості політик ---
# 0 і 3 — рідше, 1-2 — частіше
weights = [0.05, 0.3, 0.4, 0.3]  # індекси 0,1,2,3 = кількість політик

for hotel in hotels:
    hotel_name = hotel["hotel_name"]
    num_policies = random.choices([0, 1, 2, 3], weights=weights)[0]

    if num_policies == 0:
        continue  # цей готель без політик

    selected_policies = random.sample(pricing_policies, k=num_policies)
    
    for policy in selected_policies:
        hotel_pricing_policies.append({
            "hotel_name": hotel_name,
            "policy_name": policy["policy_type_name"],
            "accommodation_price_percent": policy["accommodation_price_percent"],
            "nutrition_price_percent": policy["nutrition_price_percent"]
        })

# --- Запис у JSON ---
with open("out/hotel_pricing_policies.json", "w", encoding="utf-8") as f:
    json.dump({"hotel pricing policies": hotel_pricing_policies}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(hotel_pricing_policies)} hotel pricing policy entries.")
