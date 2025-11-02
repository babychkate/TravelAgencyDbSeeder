import random
from datetime import datetime, time
from decimal import Decimal
from sql_connection import conn

# --- Функція для розрахунку актуальної ціни ---
def calculate_actual_price(expected_price, dep_dt):
    days_to_trip = (dep_dt.date() - datetime.today().date()).days
    factor = Decimal('1.3') - Decimal(days_to_trip) / Decimal(30) * Decimal('0.3')
    return Decimal(expected_price) * factor if days_to_trip <= 30 else Decimal(expected_price)

# --- Основний цикл для пакетних турів ---
with conn.cursor() as cursor:
    cursor.execute("""
        SELECT pt.package_tour_id, pt.package_tour_start_date, pt.package_tour_end_date,
               h.hotel_name, c.city_name AS hotel_city,
               ta.tour_accommodation_start_date, ta.tour_accommodation_end_date
        FROM package_tour pt
        JOIN tour_accommodation ta ON pt.tour_accommodation_id = ta.tour_accommodation_id
        JOIN room_price_season rps ON ta.room_price_season_id = rps.room_price_season_id
        JOIN tourist_season ts ON rps.tourist_season_id = ts.tourist_season_id
        JOIN hotel h ON ts.hotel_id = h.hotel_id
        JOIN city c ON h.city_id = c.city_id
        ORDER BY pt.package_tour_start_date
    """)
    tours = cursor.fetchall()

    added_bus = 0
    added_flight = 0

    for tour in tours:
        package_tour_id, tour_start, tour_end, hotel_name, hotel_city, accom_start, accom_end = tour

        # Перетворюємо дати в datetime
        tour_start = tour_start if isinstance(tour_start, datetime) else datetime.combine(tour_start, time.min)
        tour_end = tour_end if isinstance(tour_end, datetime) else datetime.combine(tour_end, time.max)

        if tour_start.date() < datetime.today().date():
            continue

        # Вибір транспорту випадково
        transport_type = random.choices(
            ["bus", "flight", "none"],
            weights=[50, 25, 25],
            k=1
        )[0]

        # --- Автобус ---
        if transport_type == "bus":
            cursor.execute("""
                SELECT bt.bus_trip_id, bt.bus_trip_expected_price, bt.bus_trip_departure_datetime, 
                       DATEADD(MINUTE, DATEDIFF(MINUTE, 0, btr.bus_trip_duration), bt.bus_trip_departure_datetime) AS bus_trip_arrival_datetime,
                       arrival_bs.bus_station_name AS arrival_station_name,
                       c.city_name AS arrival_city
                FROM bus_trip bt
                JOIN bus_trip_route btr ON bt.bus_trip_route_id = btr.bus_trip_route_id
                JOIN bus_station arrival_bs ON btr.arrival_bus_station_id = arrival_bs.bus_station_id
                JOIN city c ON arrival_bs.bus_station_city_id = c.city_id
                WHERE bt.bus_trip_departure_datetime BETWEEN ? AND ?
                ORDER BY bt.bus_trip_departure_datetime
            """, tour_start, tour_end)
            bus_trips = cursor.fetchall()

            for bt in bus_trips:
                bus_trip_id, expected_price, dep_dt, arr_dt, arrival_station, arrival_city = bt
                if arrival_city != hotel_city:
                    continue

                # Тепер перевірка транспортного перекриття тільки по туру
                if not (dep_dt >= tour_start and arr_dt <= tour_end):
                    continue

                actual_price = calculate_actual_price(expected_price, dep_dt)
                price_validation_datetime = datetime.now()

                cursor.execute("""
                    INSERT INTO bus_trip_in_tour
                    (bus_trip_id, bus_trip_in_tour_actual_price, bus_trip_in_tour_price_validation_datetime)
                    VALUES (?, ?, ?)
                """, bus_trip_id, actual_price, price_validation_datetime)
                bus_trip_in_tour_id = cursor.execute("SELECT @@IDENTITY").fetchval()

                cursor.execute("""
                    INSERT INTO package_tour_bus_trip_in_tour
                    (package_tour_id, bus_trip_in_tour_id)
                    VALUES (?, ?)
                """, package_tour_id, bus_trip_in_tour_id)

                added_bus += 1
                break
            else:
                print(f"⚠️ Не знайдено підходящий автобус для туру {package_tour_id}")

        # --- Авіарейс ---
        elif transport_type == "flight":
            cursor.execute("""
                SELECT f.flight_id, f.flight_expected_price, f.flight_departure_datetime, f.flight_arrival_datetime,
                       c.city_name AS arrival_city
                FROM flight f
                JOIN flight_route fr ON f.flight_route_id = fr.flight_route_id
                JOIN airport a ON fr.arrival_airport_id = a.airport_id
                JOIN city c ON a.airport_city_id = c.city_id
                WHERE f.flight_departure_datetime BETWEEN ? AND ?
                ORDER BY f.flight_departure_datetime
            """, tour_start, tour_end)
            flights = cursor.fetchall()

            for fl in flights:
                flight_id, expected_price, dep_dt, arr_dt, arrival_city = fl
                if arrival_city != hotel_city:
                    continue

                # Перевірка перекриття тільки по туру
                if not (dep_dt >= tour_start and arr_dt <= tour_end):
                    continue

                actual_price = calculate_actual_price(expected_price, dep_dt)
                price_validation_datetime = datetime.now()

                cursor.execute("""
                    INSERT INTO flight_in_tour
                    (flight_id, flight_in_tour_actual_price, flight_in_tour_price_validation_datetime)
                    VALUES (?, ?, ?)
                """, flight_id, actual_price, price_validation_datetime)
                flight_in_tour_id = cursor.execute("SELECT @@IDENTITY").fetchval()

                cursor.execute("""
                    INSERT INTO package_tour_flight_in_tour
                    (package_tour_id, flight_in_tour_id)
                    VALUES (?, ?)
                """, package_tour_id, flight_in_tour_id)

                added_flight += 1
                break
            else:
                print(f"⚠️ Не знайдено підходящий рейс для туру {package_tour_id}")

    conn.commit()

print(f"✅ Додано {added_bus} автобусних перевезень")
print(f"✅ Додано {added_flight} авіаперельотів")
