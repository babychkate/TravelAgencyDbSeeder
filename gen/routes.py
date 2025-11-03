import json
import random
from datetime import datetime, timedelta

# --- Зчитування класифікаторів ---
with open("in/organizations.json", "r", encoding="utf-8") as f:
    orgs = json.load(f)
    bus_companies = orgs["bus companies"]
    airlines = orgs["airlines"]

with open("in/geography.json", "r", encoding="utf-8") as f:
    geo = json.load(f)
    bus_stations = geo["bus stations"]
    airports = geo["airports"]

with open("in/classifiers.json", "r", encoding="utf-8") as f:
    classifiers = json.load(f)
    bus_route_types = classifiers["bus trip route types"]
    flight_route_types = classifiers["flight route types"]

with open("in/schedule_days.json", "r", encoding="utf-8") as f:
    schedule_days = json.load(f)["schedule days"]

with open("in/schedule_hours.json", "r", encoding="utf-8") as f:
    schedule_hours = [x["schedule_departure_time"] for x in json.load(f)["schedule hours"]]


# --- Відомі відстані між містами (км) ---
distances= {
    ("Kyiv", "Lviv"): 540,
    ("Kyiv", "Antalya"): 1800,
    ("Kyiv", "Istanbul"): 1100,
    ("Kyiv", "Hurghada"): 3000,
    ("Kyiv", "Sharm El Sheikh"): 3100,
    ("Kyiv", "Athens"): 1700,
    ("Kyiv", "Thessaloniki"): 1400,
    ("Kyiv", "Split"): 1450,
    ("Kyiv", "Dubrovnik"): 1480,
    ("Kyiv", "Budva"): 1350,
    ("Kyiv", "Podgorica"): 1380,
    ("Kyiv", "Warsaw"): 780,
    ("Kyiv", "Krakow"): 980,
    ("Kyiv", "Berlin"): 1350,
    ("Kyiv", "Munich"): 1550,
    ("Kyiv", "Paris"): 2250,
    ("Kyiv", "Nice"): 2150,
    ("Kyiv", "Barcelona"): 2800,
    ("Kyiv", "Madrid"): 3200,

    ("Lviv", "Antalya"): 2350,
    ("Lviv", "Istanbul"): 1550,
    ("Lviv", "Hurghada"): 3500,
    ("Lviv", "Sharm El Sheikh"): 3600,
    ("Lviv", "Athens"): 2150,
    ("Lviv", "Thessaloniki"): 1850,
    ("Lviv", "Split"): 1050,
    ("Lviv", "Dubrovnik"): 1100,
    ("Lviv", "Budva"): 1050,
    ("Lviv", "Podgorica"): 1080,
    ("Lviv", "Warsaw"): 390,
    ("Lviv", "Krakow"): 330,
    ("Lviv", "Berlin"): 850,
    ("Lviv", "Munich"): 1000,
    ("Lviv", "Paris"): 1600,
    ("Lviv", "Nice"): 1650,
    ("Lviv", "Barcelona"): 2300,
    ("Lviv", "Madrid"): 2750,

    ("Antalya", "Istanbul"): 720,
    ("Antalya", "Hurghada"): 1400, # (через повітря/море ~750 км), наземно - значно більше
    ("Antalya", "Sharm El Sheikh"): 1300, # (через повітря/море ~650 км), наземно - значно більше
    ("Antalya", "Athens"): 1000,
    ("Antalya", "Thessaloniki"): 1450,
    ("Antalya", "Split"): 2300,
    ("Antalya", "Dubrovnik"): 2350,
    ("Antalya", "Budva"): 2050,
    ("Antalya", "Podgorica"): 2080,
    ("Antalya", "Warsaw"): 2600,
    ("Antalya", "Krakow"): 2800,
    ("Antalya", "Berlin"): 3200,
    ("Antalya", "Munich"): 2800,
    ("Antalya", "Paris"): 3400,
    ("Antalya", "Nice"): 2600,
    ("Antalya", "Barcelona"): 3700,
    ("Antalya", "Madrid"): 4100,

    ("Istanbul", "Hurghada"): 2400, # (через повітря/море ~1400 км), наземно - значно більше
    ("Istanbul", "Sharm El Sheikh"): 2300, # (через повітря/море ~1200 км), наземно - значно більше
    ("Istanbul", "Athens"): 1100,
    ("Istanbul", "Thessaloniki"): 550,
    ("Istanbul", "Split"): 1750,
    ("Istanbul", "Dubrovnik"): 1500,
    ("Istanbul", "Budva"): 1250,
    ("Istanbul", "Podgorica"): 1280,
    ("Istanbul", "Warsaw"): 1800,
    ("Istanbul", "Krakow"): 1850,
    ("Istanbul", "Berlin"): 2150,
    ("Istanbul", "Munich"): 1950,
    ("Istanbul", "Paris"): 2750,
    ("Istanbul", "Nice"): 2300,
    ("Istanbul", "Barcelona"): 3150,
    ("Istanbul", "Madrid"): 3500,

    ("Hurghada", "Sharm El Sheikh"): 450,
    ("Hurghada", "Athens"): 1800,
    ("Hurghada", "Thessaloniki"): 2200,
    ("Hurghada", "Split"): 3400,
    ("Hurghada", "Dubrovnik"): 3500,
    ("Hurghada", "Budva"): 3200,
    ("Hurghada", "Podgorica"): 3250,
    ("Hurghada", "Warsaw"): 4000,
    ("Hurghada", "Krakow"): 4000,
    ("Hurghada", "Berlin"): 4200,
    ("Hurghada", "Munich"): 3800,
    ("Hurghada", "Paris"): 4600,
    ("Hurghada", "Nice"): 4000,
    ("Hurghada", "Barcelona"): 4800,
    ("Hurghada", "Madrid"): 5000,

    ("Sharm El Sheikh", "Athens"): 1900,
    ("Sharm El Sheikh", "Thessaloniki"): 2300,
    ("Sharm El Sheikh", "Split"): 3500,
    ("Sharm El Sheikh", "Dubrovnik"): 3600,
    ("Sharm El Sheikh", "Budva"): 3300,
    ("Sharm El Sheikh", "Podgorica"): 3350,
    ("Sharm El Sheikh", "Warsaw"): 4100,
    ("Sharm El Sheikh", "Krakow"): 4100,
    ("Sharm El Sheikh", "Berlin"): 4300,
    ("Sharm El Sheikh", "Munich"): 3900,
    ("Sharm El Sheikh", "Paris"): 4700,
    ("Sharm El Sheikh", "Nice"): 4100,
    ("Sharm El Sheikh", "Barcelona"): 4900,
    ("Sharm El Sheikh", "Madrid"): 5100,

    ("Athens", "Thessaloniki"): 500,
    ("Athens", "Split"): 1500,
    ("Athens", "Dubrovnik"): 1550,
    ("Athens", "Budva"): 1250,
    ("Athens", "Podgorica"): 1280,
    ("Athens", "Warsaw"): 2300,
    ("Athens", "Krakow"): 2200,
    ("Athens", "Berlin"): 2600,
    ("Athens", "Munich"): 1950,
    ("Athens", "Paris"): 2900,
    ("Athens", "Nice"): 2100,
    ("Athens", "Barcelona"): 3300,
    ("Athens", "Madrid"): 3600,

    ("Thessaloniki", "Split"): 950,
    ("Thessaloniki", "Dubrovnik"): 1000,
    ("Thessaloniki", "Budva"): 700,
    ("Thessaloniki", "Podgorica"): 730,
    ("Thessaloniki", "Warsaw"): 1850,
    ("Thessaloniki", "Krakow"): 1750,
    ("Thessaloniki", "Berlin"): 2100,
    ("Thessaloniki", "Munich"): 1500,
    ("Thessaloniki", "Paris"): 2400,
    ("Thessaloniki", "Nice"): 1600,
    ("Thessaloniki", "Barcelona"): 2800,
    ("Thessaloniki", "Madrid"): 3100,

    ("Split", "Dubrovnik"): 230,
    ("Split", "Budva"): 350,
    ("Split", "Podgorica"): 380,
    ("Split", "Warsaw"): 1300,
    ("Split", "Krakow"): 1100,
    ("Split", "Berlin"): 1600,
    ("Split", "Munich"): 900,
    ("Split", "Paris"): 1700,
    ("Split", "Nice"): 1000,
    ("Split", "Barcelona"): 1850,
    ("Split", "Madrid"): 2250,

    ("Dubrovnik", "Budva"): 170,
    ("Dubrovnik", "Podgorica"): 190,
    ("Dubrovnik", "Warsaw"): 1450,
    ("Dubrovnik", "Krakow"): 1250,
    ("Dubrovnik", "Berlin"): 1750,
    ("Dubrovnik", "Munich"): 1050,
    ("Dubrovnik", "Paris"): 1850,
    ("Dubrovnik", "Nice"): 1150,
    ("Dubrovnik", "Barcelona"): 2000,
    ("Dubrovnik", "Madrid"): 2400,

    ("Budva", "Podgorica"): 60,
    ("Budva", "Warsaw"): 1300,
    ("Budva", "Krakow"): 1100,
    ("Budva", "Berlin"): 1600,
    ("Budva", "Munich"): 1100,
    ("Budva", "Paris"): 1850,
    ("Budva", "Nice"): 1150,
    ("Budva", "Barcelona"): 2000,
    ("Budva", "Madrid"): 2400,

    ("Podgorica", "Warsaw"): 1350,
    ("Podgorica", "Krakow"): 1150,
    ("Podgorica", "Berlin"): 1650,
    ("Podgorica", "Munich"): 1150,
    ("Podgorica", "Paris"): 1900,
    ("Podgorica", "Nice"): 1200,
    ("Podgorica", "Barcelona"): 2050,
    ("Podgorica", "Madrid"): 2450,

    ("Warsaw", "Krakow"): 300,
    ("Warsaw", "Berlin"): 580,
    ("Warsaw", "Munich"): 1100,
    ("Warsaw", "Paris"): 1550,
    ("Warsaw", "Nice"): 1750,
    ("Warsaw", "Barcelona"): 2300,
    ("Warsaw", "Madrid"): 2700,

    ("Krakow", "Berlin"): 600,
    ("Krakow", "Munich"): 880,
    ("Krakow", "Paris"): 1400,
    ("Krakow", "Nice"): 1550,
    ("Krakow", "Barcelona"): 2100,
    ("Krakow", "Madrid"): 2500,

    ("Berlin", "Munich"): 580,
    ("Berlin", "Paris"): 1050,
    ("Berlin", "Nice"): 1550,
    ("Berlin", "Barcelona"): 1850,
    ("Berlin", "Madrid"): 2300,

    ("Munich", "Paris"): 820,
    ("Munich", "Nice"): 800,
    ("Munich", "Barcelona"): 1350,
    ("Munich", "Madrid"): 1850,

    ("Paris", "Nice"): 930,
    ("Paris", "Barcelona"): 1050,
    ("Paris", "Madrid"): 1250,

    ("Nice", "Barcelona"): 660,
    ("Nice", "Madrid"): 1250,

    ("Barcelona", "Madrid"): 620
}

def get_distance(dep, arr):
    if dep == arr:
        return 50
    return distances.get((dep, arr)) or distances.get((arr, dep)) or random.randint(200, 2000)

def pick_route_type_by_distance(dist_km, mode="bus"):
    if mode == "bus":
        if dist_km >= 700:
            return random.choices(bus_route_types, weights=[0.35,0.15,0.5])[0]
        if dist_km >= 300:
            return random.choices(bus_route_types, weights=[0.6,0.15,0.25])[0]
        return random.choices(bus_route_types, weights=[0.6,0.3,0.1])[0]
    else:
        if dist_km >= 1500:
            return random.choices(flight_route_types, weights=[0.2,0.6,0.2])[0]
        if dist_km >= 800:
            return random.choices(flight_route_types, weights=[0.3,0.4,0.3])[0]
        return random.choices(flight_route_types, weights=[0.3,0.1,0.6])[0]

def calculate_duration(dist_km, mode="bus"):
    speed = 80 if mode == "bus" else 700  # км/год
    hours = dist_km / speed
    duration_hours = int(hours)
    duration_minutes = int((hours - duration_hours) * 60)
    return timedelta(hours=duration_hours, minutes=duration_minutes)

def pick_departure_time(duration, schedule_hours):
    """Обираємо час відправлення та обмежуємо тривалість до 23:59"""
    dep_time_str = random.choice(schedule_hours)
    dep_time = datetime.strptime(dep_time_str, "%H:%M")
    arr_time = dep_time + duration

    max_duration = timedelta(hours=23, minutes=59)
    if duration > max_duration:
        duration = max_duration
        arr_time = dep_time + duration

    return dep_time.time(), arr_time.time(), duration

# --- Генерація маршрутів ---
routes = []
num_bus_routes = 40
num_flight_routes = 40

# --- Генерація автобусних маршрутів ---
bus_routes = []
for i in range(num_bus_routes):
    dep, arr = random.sample(bus_stations, 2)
    company = random.choice(bus_companies)
    dist = get_distance(dep["city_name"], arr["city_name"])
    duration = calculate_duration(dist, "bus")
    dep_time, arr_time, duration = pick_departure_time(duration, schedule_hours)
    route_type = pick_route_type_by_distance(dist, "bus")
    route_num = f"R-{i+1:05d}"

    bus_routes.append({
        "route_number": route_num,
        "bus_trip_duration": str(duration),
        "bus_trip_route_type_name": route_type,
        "departure_bus_station_name": dep["city_name"],
        "arrival_bus_station_name": arr["city_name"],
        "bus_company_name": company,
        "departure_time": dep_time.strftime("%H:%M"),
        "arrival_time": arr_time.strftime("%H:%M")
    })

# --- Генерація авіаційних маршрутів ---
flight_routes = []
for i in range(num_flight_routes):
    dep, arr = random.sample(airports, 2)
    company = random.choice(airlines)
    dist = get_distance(dep["city_name"], arr["city_name"])
    duration = calculate_duration(dist, "flight")
    dep_time, arr_time, duration = pick_departure_time(duration, schedule_hours)
    route_type = pick_route_type_by_distance(dist, "flight")
    route_num = f"F-{i+1:05d}"

    flight_routes.append({
        "route_number": route_num,
        "flight_duration": str(duration),
        "flight_route_type_name": route_type,
        "departure_airport_name": dep["city_name"],
        "arrival_airport_name": arr["city_name"],
        "airline_name": company,
        "departure_time": dep_time.strftime("%H:%M"),
        "arrival_time": arr_time.strftime("%H:%M")
    })

# --- Збереження у JSON ---
output = {
    "bus trip routes": bus_routes,
    "flight routes": flight_routes
}

with open("out/routes.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Збережено {len(bus_routes)} автобусних і {len(flight_routes)} авіарейсних маршрутів.")