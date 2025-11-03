import json

# --- Читаємо маршрути ---
with open("out/routes.json", "r", encoding="utf-8") as f:
    routes_data = json.load(f)
    bus_routes = routes_data.get("bus trip routes", [])
    flight_routes = routes_data.get("flight routes", [])

# --- Генерація schedule_hours у потрібному форматі ---
def generate_schedule_hours(routes, dep_field, arr_field):
    schedule_hours = []
    for r in routes:
        schedule_hours.append({
            "schedule_departure_time": r[dep_field],
            "schedule_arrival_time": r[arr_field]
        })
    # унікальні значення
    seen = set()
    unique_schedule_hours = []
    for sh in schedule_hours:
        tup = (sh["schedule_departure_time"], sh["schedule_arrival_time"])
        if tup not in seen:
            seen.add(tup)
            unique_schedule_hours.append(sh)
    return unique_schedule_hours

bus_schedule_hours = generate_schedule_hours(bus_routes, "departure_time", "arrival_time")
flight_schedule_hours = generate_schedule_hours(flight_routes, "departure_time", "arrival_time")

# --- Збереження ---
with open("out/schedule_hours.json", "w", encoding="utf-8") as f:
    json.dump({
        "bus schedule hours": bus_schedule_hours,
        "flight schedule hours": flight_schedule_hours
    }, f, ensure_ascii=False, indent=2)

print(f"Згенеровано {len(bus_schedule_hours)} автобусних та {len(flight_schedule_hours)} авіаційних годин.")
