from backend.app.models import AircraftBase
from seed_all import seed_all

aircraft_data = [
    {"model": "Boeing 737", "capacity": 160, "registration_number": 10001},
    {"model": "Airbus A320", "capacity": 150, "registration_number": 10002},
    {"model": "Embraer E190", "capacity": 100, "registration_number": 10003},
    {"model": "Boeing 777", "capacity": 300, "registration_number": 10004},
    {"model": "Airbus A350", "capacity": 310, "registration_number": 10005},
    {"model": "Bombardier Q400", "capacity": 78, "registration_number": 10006},
    {"model": "ATR 72", "capacity": 70, "registration_number": 10007},
    {"model": "Boeing 787", "capacity": 242, "registration_number": 10008},
    {"model": "Airbus A330", "capacity": 277, "registration_number": 10009},
    {"model": "Sukhoi Superjet 100", "capacity": 98, "registration_number": 10010},
]


async def seed_aircraft():
    await seed_all(AircraftBase, aircraft_data)
