import random
from datetime import datetime, timedelta
from decimal import Decimal
from sql_connection import conn

random.seed(42)

# --- Константи політик ---
EARLY_BIRD_DAYS = 45
LAST_MINUTE_DAYS = 7

with conn.cursor() as cursor:
    # --- Зчитуємо менеджерів ---
    cursor.execute("SELECT travel_agency_manager_id FROM travel_agency_manager")
    managers = [row[0] for row in cursor.fetchall()]

    # --- Зчитуємо пакетні тури ---
    cursor.execute("""
        SELECT 
            pt.package_tour_id,
            pt.tour_accommodation_id,
            pt.package_tour_start_date,
            pt.package_tour_end_date,
            pt.package_tour_max_tourists_count,
            ta.room_price_season_id,
            ta.meal_price_season_id,
            h.hotel_id,
            hpr.pricing_policy_id,
            hrt.hotel_room_type_max_adults,
            hrt.hotel_room_type_max_children,
            rps.room_price_per_person,
            mps.meal_price_per_person
        FROM package_tour pt
        JOIN tour_accommodation ta ON ta.tour_accommodation_id = pt.tour_accommodation_id
        JOIN room_price_season rps ON rps.room_price_season_id = ta.room_price_season_id
        JOIN hotel_room_type hrt ON hrt.hotel_room_type_id = rps.hotel_room_type_id
        JOIN tourist_season ts ON ts.tourist_season_id = rps.tourist_season_id
        JOIN hotel h ON h.hotel_id = ts.hotel_id
        JOIN meal_price_season mps ON mps.meal_price_season_id = ta.meal_price_season_id
        JOIN hotel_pricing_policy hpr ON hpr.hotel_id = h.hotel_id
    """)
    package_tours = cursor.fetchall()

    # --- Зчитуємо пасажирів ---
    cursor.execute("SELECT passenger_id FROM passenger")
    passengers = [row[0] for row in cursor.fetchall()]

    bookings_generated = 0

    for pt in package_tours:
        (package_tour_id, tour_accommodation_id, tour_start_str, tour_end_str,
         max_tourists, room_price_season_id, meal_price_season_id,
         hotel_id, pricing_policy_id,
         max_adults, max_children,
         room_price, meal_price) = pt

        tour_start = datetime.strptime(str(tour_start_str), "%Y-%m-%d")
        tour_end = datetime.strptime(str(tour_end_str), "%Y-%m-%d")
        stay_days = (tour_end - tour_start).days

        booking_date = tour_start - timedelta(days=random.randint(1, 60))

        adults_count = random.randint(1, max_adults)
        children_count = random.randint(0, max_children)
        if adults_count + children_count > max_adults + max_children:
            children_count = (max_adults + max_children) - adults_count

        # --- Ціна проживання ---
        cursor.execute("""
            SELECT policy_type_id, accommodation_price_percent, nutrition_price_percent 
            FROM pricing_policy WHERE pricing_policy_id = ?
        """, pricing_policy_id)
        policy_type_id, acc_percent, nutr_percent = cursor.fetchone()

        total_room = Decimal(adults_count + children_count) * Decimal(room_price)
        total_meal = Decimal(adults_count + children_count) * Decimal(meal_price)

        if policy_type_id == 1 and (tour_start - booking_date).days > EARLY_BIRD_DAYS:
            total_room *= Decimal(acc_percent)
            total_meal *= Decimal(nutr_percent)
        elif policy_type_id == 2:
            total_room = adults_count*Decimal(room_price) + children_count*Decimal(room_price)*Decimal(acc_percent)
            total_meal = adults_count*Decimal(meal_price) + children_count*Decimal(meal_price)*Decimal(nutr_percent)
        elif policy_type_id == 3 and (tour_start - booking_date).days < LAST_MINUTE_DAYS:
            total_room *= Decimal(acc_percent)
            total_meal *= Decimal(nutr_percent)

        total_accommodation_price = (total_room + total_meal) * stay_days

        # --- Ціна транспорту ---
        cursor.execute("""
            SELECT bti.bus_trip_id, bti.bus_trip_in_tour_actual_price
            FROM package_tour_bus_trip_in_tour ptb
            JOIN bus_trip_in_tour bti ON bti.bus_trip_in_tour_id = ptb.bus_trip_in_tour_id
            WHERE ptb.package_tour_id = ?
        """, package_tour_id)
        bus_trip_data = cursor.fetchone()
        transport_price = Decimal('0')

        if bus_trip_data:
            bus_trip_id, actual_price = bus_trip_data
            days_before = (tour_start - booking_date).days
            # логіка раннього/останніх днів для транспорту
            if days_before > EARLY_BIRD_DAYS:
                transport_price = Decimal(actual_price) * Decimal('0.9')
            elif days_before < LAST_MINUTE_DAYS:
                transport_price = Decimal(actual_price) * Decimal('1.2')
            else:
                transport_price = Decimal(actual_price)

        total_price = total_accommodation_price + transport_price

        # --- Випадковий менеджер ---
        travel_agency_manager_id = random.choice(managers)

        # --- Insert booking ---
        cursor.execute("""
            INSERT INTO booking (
                travel_agency_manager_id,
                package_tour_id,
                booking_status_id,
                booking_adults_count,
                booking_children_count,
                booking_date,
                booking_total_price
            ) OUTPUT INSERTED.booking_id
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            travel_agency_manager_id,
            package_tour_id,
            1,
            adults_count,
            children_count,
            booking_date.strftime("%Y-%m-%d"),
            total_price
        ))
        booking_id = cursor.fetchone()[0]

        # --- Прив’язка пасажирів ---
        selected_passengers = random.sample(passengers, adults_count + children_count)
        for pid in selected_passengers:
            cursor.execute("""
                INSERT INTO booking_passenger (booking_id, passenger_id)
                VALUES (?, ?)
            """, (booking_id, pid))

        bookings_generated += 1

    conn.commit()
    print(f"✅ Згенеровано {bookings_generated} бронювань.")
