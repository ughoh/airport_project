from datetime import date
from backend.app.models import PassengerGender, PassengerBase
from seed_all import seed_all

passenger_data = [
    {
        "first_name": "Anna",
        "last_name": "Ivanova",
        "gender": PassengerGender.female,
        "date_of_birth": date(1995, 4, 15)
    },
    {
        "first_name": "Oleh",
        "last_name": "Shevchenko",
        "gender": PassengerGender.male,
        "date_of_birth": date(1988, 9, 23)
    },
    {
        "first_name": "Kateryna",
        "last_name": "Poliakova",
        "gender": PassengerGender.female,
        "date_of_birth": date(2000, 1, 5)
    },
    {
        "first_name": "Ivan",
        "last_name": "Tkachenko",
        "gender": PassengerGender.male,
        "date_of_birth": date(1975, 7, 12)
    },
    {
        "first_name": "Dmytro",
        "last_name": "Bondarenko",
        "gender": PassengerGender.male,
        "date_of_birth": date(1992, 11, 30)
    },
    {
        "first_name": "Olha",
        "last_name": "Melnyk",
        "gender": PassengerGender.female,
        "date_of_birth": date(1985, 5, 19)
    },
    {
        "first_name": "Yurii",
        "last_name": "Koval",
        "gender": PassengerGender.undefined,
        "date_of_birth": date(1990, 3, 8)
    },
    {
        "first_name": "Svitlana",
        "last_name": "Savchenko",
        "gender": PassengerGender.female,
        "date_of_birth": date(1999, 12, 25)
    },
    {
        "first_name": "Andrii",
        "last_name": "Hnatenko",
        "gender": PassengerGender.male,
        "date_of_birth": date(1983, 6, 2)
    },
    {
        "first_name": "Natalia",
        "last_name": "Rudenko",
        "gender": PassengerGender.female,
        "date_of_birth": date(2001, 8, 10)
    },
]


async def seed_passengers():
    await seed_all(PassengerBase,passenger_data)
