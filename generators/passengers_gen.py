from faker import Faker
import json
import random
import string

fake = Faker()

num_passengers = 27000
passengers = []

for i in range(1, num_passengers + 1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    birth_date = fake.date_between(start_date='-75y', end_date='-15y')  # між 1950 і 2010
    if random.choice([True, False]):
        passport_number = ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=6))
    else:
        passport_number = ''.join(random.choices(string.digits, k=9))
    
    passengers.append({
        "passenger_first_name": first_name,
        "passenger_last_name": last_name,
        "passenger_birth_date": str(birth_date),
        "passenger_passport_number": passport_number
    })

with open('passengers.json', 'w', encoding='utf-8') as f:
    json.dump({"passengers": passengers}, f, ensure_ascii=False, indent=4)

print(f'{num_passengers} passengers generated and saved to passengers.json')
