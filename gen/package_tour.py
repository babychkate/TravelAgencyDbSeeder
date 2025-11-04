import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Параметри ---
max_tourists_multiplier = 1
max_trips_per_accommodation = 5  # скільки рейсів беремо для кожного проживання

# --- Зчитування даних ---
with open(base_path / "out/bus_trip.json", "r", encoding="utf-8") as f:
    bus_trips = json.load(f)["bus trips"]

with open(base_path / "out/flight.json", "r", encoding="utf-8") as f:
    flight_trips = json.load(f)["flights"]

with open(base_path / "out/routes.json", "r", encoding="utf-8") as f:
    bus_trip_routes = json.load(f)["bus trip routes"]

with open(base_path / "out/routes.json", "r", encoding="utf-8") as f:
    flight_trip_routes = json.load(f)["flight routes"]

with open(base_path / "out/tour_accommodations.json", "r", encoding="utf-8") as f:
    accommodations = json.load(f)["tour accommodations"]

with open(base_path / "in/hotels.json", "r", encoding="utf-8") as f:
    hotels = json.load(f)["hotels"]

with open(base_path / "in/organizations.json", "r", encoding="utf-8") as f:
    organizations = json.load(f)["tour operators"]

# --- Створюємо mapping готель → місто ---
hotel_name_to_city = {h["hotel_name"]: h["city_name"] for h in hotels}

# --- Створюємо mapping route_number → route info ---
bus_route_mapping = {r["route_number"]: r for r in bus_trip_routes}
flight_route_mapping = {r["route_number"]: r for r in flight_trip_routes}

# --- Додаємо міста до trips ---
for t in bus_trips:
    route_info = bus_route_mapping.get(t["route_number"])
    if route_info:
        t["from_city"] = route_info["departure_city_name"]
        t["to_city"] = route_info["arrival_city_name"]

for t in flight_trips:
    route_info = flight_route_mapping.get(t["route_number"])
    if route_info:
        t["from_city"] = route_info["departure_city_name"]
        t["to_city"] = route_info["arrival_city_name"]

# --- Списки для генерації назв та описів ---
tour_name_adjectives = [
    "Luxury", "Adventure", "Romantic", "Family", "Exclusive", "Relaxing", "Exciting",
    "Cultural", "Scenic", "Unforgettable", "Gourmet", "Wellness", "Active", "Charming",
    "Breathtaking", "Historical", "Tranquil", "Vibrant", "Nature", "Epic"
]

tour_name_nouns = [
    "Escape", "Journey", "Experience", "Getaway", "Retreat", "Holiday", "Tour",
    "Adventure", "Odyssey", "Expedition", "Excursion", "Voyage", "Quest", "Trip",
    "Sojourn", "Exploration", "Break", "Safari", "Discovery"
]

tour_description_templates = [
    "Enjoy a {adjective} stay at {hotel} with comfort and style.",
    "This {adjective} tour offers relaxation and unforgettable experiences at {hotel}.",
    "Perfect for families, the {adjective} getaway at {hotel} includes meals and comfortable rooms.",
    "Experience {adjective} moments at {hotel} with top-notch services and amenities.",
    "Discover the beauty of {hotel} in this {adjective} travel experience.",
    "Make your stay {adjective} at {hotel} with luxurious accommodations and personalized service.",
    "Embark on a {adjective} journey at {hotel} and explore local attractions.",
    "Enjoy {adjective} adventures and leisure at {hotel}, perfect for all travelers.",
    "Relax and unwind with a {adjective} escape at {hotel}.",
    "The {adjective} retreat at {hotel} guarantees unforgettable memories.",
    "Stay {adjective} at {hotel} and indulge in fine dining and spa experiences.",
    "Discover {adjective} comfort and elegance at {hotel} during your stay.",
    "Experience the {adjective} charm of {hotel} and enjoy premium amenities.",
    "A {adjective} holiday at {hotel} awaits with exciting activities and cozy rooms.",
    "Feel {adjective} moments at {hotel} with beautiful views and relaxing ambiance.",
    "Plan a {adjective} vacation at {hotel} full of comfort, fun, and culinary delights.",
    "Enjoy a {adjective} blend of relaxation and adventure at {hotel}.",
    "Stay {adjective} at {hotel} with family-friendly facilities and entertainment options.",
    "The {adjective} experience at {hotel} combines style, comfort, and excellent service.",
    "Make your trip {adjective} with an unforgettable stay at {hotel}."
]

# --- Допоміжні функції ---
def random_operator():
    return random.choice(organizations)

def random_tour_name(index):
    adjective = random.choice(tour_name_adjectives)
    noun = random.choice(tour_name_nouns)
    return f"{adjective} {noun} #{str(index).zfill(4)}"

def random_description(hotel_name):
    template = random.choice(tour_description_templates)
    adjective = random.choice(tour_name_adjectives)
    return template.format(adjective=adjective, hotel=hotel_name)

# --- Генерація пакетних турів ---
package_tours = []
tour_index = 1

for acc in accommodations:
    max_tourists = acc["max_adults"] + acc.get("max_children", 0)

    hotel_city = hotel_name_to_city.get(acc["hotel_name"])
    if not hotel_city:
        continue  # пропускаємо, якщо міста немає

    acc_start = datetime.strptime(acc["tour_accommodation_start_date"], "%Y-%m-%d")
    acc_end = datetime.strptime(acc["tour_accommodation_end_date"], "%Y-%m-%d")

    matching_bus_trips = [
        t for t in bus_trips
        if t.get("to_city") == hotel_city
        and acc_start - timedelta(days=1) <= datetime.strptime(t["date"], "%Y-%m-%d") <= acc_start
    ]

    matching_flight_trips = [
        t for t in flight_trips
        if t.get("to_city") == hotel_city
        and acc_start - timedelta(days=1) <= datetime.strptime(t["date"], "%Y-%m-%d") <= acc_start
    ]

    all_matching_trips = matching_bus_trips + matching_flight_trips
    if not all_matching_trips:
        continue

    selected_trips = random.sample(
        all_matching_trips,
        k=min(max_trips_per_accommodation, len(all_matching_trips))
    )

    for t in selected_trips:
        trip_type = "bus" if t in matching_bus_trips else "flight"

        tour_start = datetime.strptime(t["date"], "%Y-%m-%d")

        dep_time = datetime.strptime(t[f"{trip_type}_trip_departure_time"], "%H:%M")
        arr_time = datetime.strptime(t[f"{trip_type}_trip_arrival_time"], "%H:%M")
        duration = arr_time - dep_time
        if duration.total_seconds() < 0:
            duration += timedelta(days=1)
        tour_end = acc_end + duration

        package_tours.append({
            "tour_operator_name": random_operator(),
            "tour_accommodation": acc,
            "tour_transport": {
                "transport_type": trip_type,
                "route_number": t["route_number"],
                "date": t["date"],
                "from_city": t["from_city"],
                "to_city": t["to_city"],
                "departure_time": t[f"{trip_type}_trip_departure_time"],
                "arrival_time": t[f"{trip_type}_trip_arrival_time"],
                "expected_price": t.get(f"{trip_type}_trip_expected_price")
            },
            "package_tour_status_name": "Active",
            "package_tour_name": random_tour_name(tour_index),
            "package_tour_description": random_description(acc["hotel_name"]),
            "package_tour_start_date": tour_start.strftime("%Y-%m-%d"),
            "package_tour_end_date": tour_end.strftime("%Y-%m-%d"),
            "package_tour_max_tourists_count": max_tourists * max_tourists_multiplier
        })
        tour_index += 1

# --- Збереження ---
output_path = base_path / "out"
output_path.mkdir(exist_ok=True)
with open(output_path / "package_tours.json", "w", encoding="utf-8") as f:
    json.dump({"package tours": package_tours}, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(package_tours)} пакетних турів")
