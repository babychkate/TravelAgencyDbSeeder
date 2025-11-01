import random
from datetime import datetime
from decimal import Decimal
from sql_connection import conn

with conn.cursor() as cursor:
    # Беремо всі тури
    cursor.execute("SELECT package_tour_id, package_tour_start_date, package_tour_end_date FROM package_tour")
    tours = cursor.fetchall()

    added_bus = 0
    added_flight = 0

    for tour in tours:
        package_tour_id, start_date, end_date = tour
        start_date = start_date.date() if isinstance(start_date, datetime) else start_date
        end_date = end_date.date() if isinstance(end_date, datetime) else end_date

        # Перевірка: тур ще не почався
        if start_date < datetime.today().date():
            continue

        # Вибір типу транспорту за шансами 50/25/25
        chance = random.randint(1, 100)
        transport_type = None
        if chance <= 50:
            transport_type = "bus"
        elif chance <= 75:
            transport_type = "flight"
        else:
            transport_type = "none"

        if transport_type == "bus":
            cursor.execute("SELECT bus_trip_id, bus_trip_expected_price, bus_trip_departure_datetime, bus_trip_arrival_datetime FROM bus_trip ORDER BY bus_trip_departure_datetime")
            bus_trips = cursor.fetchall()
            for bus_row in bus_trips:
                bus_trip_id, expected_price, dep_dt, arr_dt = bus_row
                if start_date <= dep_dt.date() <= end_date and arr_dt.date() <= end_date:
                    days_to_trip = (dep_dt.date() - datetime.today().date()).days
                    if days_to_trip < 0:
                        continue
                    elif days_to_trip > 30:
                        actual_price = expected_price
                    else:
                        multiplier = Decimal('1') + Decimal('0.3') * (Decimal('1') - Decimal(days_to_trip)/Decimal('30'))
                        actual_price = Decimal(expected_price) * multiplier

                    price_validation_datetime = datetime.now()

                    # Вставка в bus_trip_in_tour
                    cursor.execute("""
                        INSERT INTO bus_trip_in_tour
                        (bus_trip_id, bus_trip_in_tour_actual_price, bus_trip_in_tour_price_validation_datetime)
                        VALUES (?, ?, ?)
                    """, bus_trip_id, actual_price, price_validation_datetime)
                    bus_trip_in_tour_id = cursor.execute("SELECT @@IDENTITY").fetchval()

                    # Прив'язка до туру
                    cursor.execute("""
                        INSERT INTO package_tour_bus_trip_in_tour
                        (package_tour_id, bus_trip_in_tour_id)
                        VALUES (?, ?)
                    """, package_tour_id, bus_trip_in_tour_id)

                    added_bus += 1
                    break  # беремо перший підходящий автобус

        elif transport_type == "flight":
            cursor.execute("SELECT flight_id, flight_expected_price, flight_departure_datetime, flight_arrival_datetime FROM flight ORDER BY flight_departure_datetime")
            flights = cursor.fetchall()
            for flight_row in flights:
                flight_id, expected_price, dep_dt, arr_dt = flight_row
                if start_date <= dep_dt.date() <= end_date and arr_dt.date() <= end_date:
                    days_to_trip = (dep_dt.date() - datetime.today().date()).days
                    if days_to_trip < 0:
                        continue
                    elif days_to_trip > 30:
                        actual_price = expected_price
                    else:
                        multiplier = Decimal('1') + Decimal('0.3') * (Decimal('1') - Decimal(days_to_trip)/Decimal('30'))
                        actual_price = Decimal(expected_price) * multiplier

                    price_validation_datetime = datetime.now()

                    # Вставка в flight_in_tour
                    cursor.execute("""
                        INSERT INTO flight_in_tour
                        (flight_id, flight_in_tour_actual_price, flight_in_tour_price_validation_datetime)
                        VALUES (?, ?, ?)
                    """, flight_id, actual_price, price_validation_datetime)
                    flight_in_tour_id = cursor.execute("SELECT @@IDENTITY").fetchval()

                    # Прив'язка до туру
                    cursor.execute("""
                        INSERT INTO package_tour_flight_in_tour
                        (package_tour_id, flight_in_tour_id)
                        VALUES (?, ?)
                    """, package_tour_id, flight_in_tour_id)

                    added_flight += 1
                    break  # беремо перший підходящий рейс

    conn.commit()

print(f"✅ Додано {added_bus} автобусних перевезень")
print(f"✅ Додано {added_flight} авіаперельотів")
