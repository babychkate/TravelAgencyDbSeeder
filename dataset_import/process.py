import random
from datetime import datetime, timedelta
from sql_connection import conn

random.seed(42)

# Константи політик
EARLY_BIRD_DAYS = 45
LAST_MINUTE_DAYS = 7

with conn.cursor() as cursor:
    # --- Зчитуємо package tours ---
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

        # Дата туру
        tour_start = datetime.strptime(str(tour_start_str), "%Y-%m-%d")
        tour_end = datetime.strptime(str(tour_end_str), "%Y-%m-%d")

        # Генеруємо дату бронювання до 60 днів перед туром
        booking_date = tour_start - timedelta(days=random.randint(1, 60))

        # Випадкова кількість дорослих і дітей
        adults_count = random.randint(1, max_adults)
        children_count = random.randint(0, max_children)
        if adults_count + children_count > max_adults + max_children:
            children_count = (max_adults + max_children) - adults_count

        # --- Калькуляція ціни з урахуванням політики ---
        cursor.execute("""
            SELECT policy_type_id, accommodation_price_percent, nutrition_price_percent 
            FROM pricing_policy 
            WHERE pricing_policy_id = ?
        """, pricing_policy_id)
        policy = cursor.fetchone()
        policy_type_id, acc_percent, nutr_percent = policy

        total_room = (adults_count + children_count) * room_price
        total_meal = (adults_count + children_count) * meal_price

        # Early bird / Last minute / Child discount
        if policy_type_id == 1 and (tour_start - booking_date).days > EARLY_BIRD_DAYS:  # Early bird
            total_room *= acc_percent
            total_meal *= nutr_percent
        elif policy_type_id == 2:  # Child discount
            total_room = adults_count*room_price + children_count*room_price*acc_percent
            total_meal = adults_count*meal_price + children_count*meal_price*nutr_percent
        elif policy_type_id == 3 and (tour_start - booking_date).days < LAST_MINUTE_DAYS:  # Last minute
            total_room *= acc_percent
            total_meal *= nutr_percent

        total_price = total_room + total_meal

        cursor.execute("""
            INSERT INTO booking (
                travel_agency_manager_id,
                package_tour_id,
                booking_status_id,
                booking_adults_count,
                booking_children_count,
                booking_date,
                booking_total_price
            )
            OUTPUT INSERTED.booking_id
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (1, package_tour_id, 1, adults_count, children_count, booking_date.strftime("%Y-%m-%d"), total_price))
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
