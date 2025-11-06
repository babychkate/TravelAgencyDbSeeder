import json
import random
from datetime import datetime, timedelta
from pathlib import Path

base_path = Path(__file__).parent.parent

# --- Параметри ---
max_tourists_multiplier = 15
max_trips_per_accommodation = 5
skip_transport_probability = 0.30  # 20% турів без транспорту

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

# --- Mapping ---
hotel_name_to_city = {h["hotel_name"]: h["city_name"] for h in hotels}
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

# --- Генератори назв та описів ---
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

# --- Шаблони опису для турів без транспорту ---
tour_description_no_transport_templates = [
    "Enjoy a {adjective} stay at {hotel} with comfort and style.",
    "Relax at {hotel} in this {adjective} accommodation, perfect for all guests.",
    "Experience {adjective} moments at {hotel} with premium amenities.",
    "Stay {adjective} at {hotel} and enjoy local attractions and cozy rooms.",
    "The {adjective} retreat at {hotel} ensures comfort and relaxation.",
    "Plan a {adjective} vacation at {hotel} full of comfort and leisure.",
    "Discover {adjective} comfort and elegance at {hotel} during your stay.",
    "Enjoy a {adjective} escape at {hotel} with fine dining and spa services."
]

# --- Допоміжні функції ---
def random_operator():
    return random.choice(organizations)

def random_tour_name(index):
    adjective = random.choice(tour_name_adjectives)
    noun = random.choice(tour_name_nouns)
    return f"{adjective} {noun}"

def random_description(hotel_name, has_transport=True):
    adjective = random.choice(tour_name_adjectives)
    if has_transport:
        template = random.choice(tour_description_templates)
    else:
        template = random.choice(tour_description_no_transport_templates)
    return template.format(adjective=adjective, hotel=hotel_name)

# --- Генерація пакетних турів ---
package_tours = []
tour_index = 1

for acc in accommodations:
    max_tourists = acc["max_adults"] + acc.get("max_children", 0)
    hotel_city = hotel_name_to_city.get(acc["hotel_name"])
    if not hotel_city:
        continue

    acc_start = datetime.strptime(acc["tour_accommodation_start_date"], "%Y-%m-%d")
    acc_end = datetime.strptime(acc["tour_accommodation_end_date"], "%Y-%m-%d")

    # --- Пошук рейсів ---
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

    # --- Випадкове рішення: чи буде транспорт ---
    has_transport = all_matching_trips and random.random() > skip_transport_probability

    if has_transport:
        selected_trips = random.sample(
            all_matching_trips,
            k=min(max_trips_per_accommodation, len(all_matching_trips))
        )
    else:
        selected_trips = [None]  # тур без транспорту

    # --- Створюємо тур(и) ---
    for t in selected_trips:
        if t:
            trip_type = "bus" if t in matching_bus_trips else "flight"
            
            dep_time = datetime.strptime(t[f"{trip_type}_trip_departure_time"], "%H:%M")
            arr_time = datetime.strptime(t[f"{trip_type}_trip_arrival_time"], "%H:%M")

            # Об'єднуємо з датою проживання
            dep_datetime = datetime.combine(acc_start, dep_time.time())
            arr_datetime = datetime.combine(acc_start, arr_time.time())

            # Якщо приїзд раніше від виїзду, додаємо добу
            if arr_datetime < dep_datetime:
                arr_datetime += timedelta(days=1)

            # Початок туру
            tour_start = acc_start
            if dep_datetime.date() < acc_start.date() or dep_datetime.hour >= 18:
                # виїзд пізно ввечері → тур починається попереднього дня
                tour_start -= timedelta(days=1)

            # Кінець туру
            tour_end = acc_end
            if arr_datetime.date() > acc_start.date():
                # приїзд після півночі → додаємо день до кінця туру
                tour_end += timedelta(days=(arr_datetime.date() - acc_start.date()).days)

            transport_info = {
                "transport_type": trip_type,
                "route_number": t["route_number"],
                "date": t["date"],
                "from_city": t["from_city"],
                "to_city": t["to_city"],
                "departure_time": t[f"{trip_type}_trip_departure_time"],
                "arrival_time": t[f"{trip_type}_trip_arrival_time"],
                "expected_price": t.get(f"{trip_type}_trip_expected_price")
            }
        else:
            # Без транспорту → дати = проживання
            tour_start = acc_start
            tour_end = acc_end
            transport_info = None

        package_tours.append({
            "tour_operator_name": random_operator(),
            "tour_accommodation": acc,
            "tour_transport": transport_info,
            "package_tour_status_name": "Active",
            "package_tour_name": random_tour_name(tour_index),
            "package_tour_description": random_description(acc["hotel_name"], has_transport=has_transport),
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
