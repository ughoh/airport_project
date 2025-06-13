from datetime import datetime, timedelta
from backend.app.models import FlightStatus, FlightBase
from seed_all import seed_all

flight_data = [
    {
        "airline_id": 1,
        "aircraft_id": 1,
        "departure_airport_id": 1,
        "arrival_airport_id": 2,
        "departure_time": datetime.now() + timedelta(days=1, hours=2),
        "arrival_time": datetime.now() + timedelta(days=1, hours=5),
        "status": FlightStatus.planned
    },
    {
        "airline_id": 2,
        "aircraft_id": 2,
        "departure_airport_id": 3,
        "arrival_airport_id": 4,
        "departure_time": datetime.now() + timedelta(days=2, hours=4),
        "arrival_time": datetime.now() + timedelta(days=2, hours=8),
        "status": FlightStatus.delayed
    },
    {
        "airline_id": 3,
        "aircraft_id": 3,
        "departure_airport_id": 2,
        "arrival_airport_id": 5,
        "departure_time": datetime.now() + timedelta(days=3, hours=1),
        "arrival_time": datetime.now() + timedelta(days=3, hours=6),
        "status": FlightStatus.canceled
    },
    {
        "airline_id": 1,
        "aircraft_id": 4,
        "departure_airport_id": 4,
        "arrival_airport_id": 1,
        "departure_time": datetime.now() + timedelta(days=4, hours=3),
        "arrival_time": datetime.now() + timedelta(days=4, hours=7),
        "status": FlightStatus.planned
    },
    {
        "airline_id": 2,
        "aircraft_id": 5,
        "departure_airport_id": 5,
        "arrival_airport_id": 3,
        "departure_time": datetime.now() + timedelta(days=5, hours=2),
        "arrival_time": datetime.now() + timedelta(days=5, hours=6),
        "status": FlightStatus.planned
    },
    {
        "airline_id": 3,
        "aircraft_id": 6,
        "departure_airport_id": 1,
        "arrival_airport_id": 4,
        "departure_time": datetime.now() + timedelta(days=6, hours=5),
        "arrival_time": datetime.now() + timedelta(days=6, hours=10),
        "status": FlightStatus.delayed
    },
    {
        "airline_id": 1,
        "aircraft_id": 7,
        "departure_airport_id": 2,
        "arrival_airport_id": 3,
        "departure_time": datetime.now() + timedelta(days=7, hours=4),
        "arrival_time": datetime.now() + timedelta(days=7, hours=8),
        "status": FlightStatus.planned
    },
    {
        "airline_id": 2,
        "aircraft_id": 8,
        "departure_airport_id": 3,
        "arrival_airport_id": 5,
        "departure_time": datetime.now() + timedelta(days=8, hours=1),
        "arrival_time": datetime.now() + timedelta(days=8, hours=7),
        "status": FlightStatus.canceled
    },
    {
        "airline_id": 3,
        "aircraft_id": 9,
        "departure_airport_id": 4,
        "arrival_airport_id": 2,
        "departure_time": datetime.now() + timedelta(days=9, hours=3),
        "arrival_time": datetime.now() + timedelta(days=9, hours=8),
        "status": FlightStatus.planned
    },
    {
        "airline_id": 1,
        "aircraft_id": 10,
        "departure_airport_id": 5,
        "arrival_airport_id": 1,
        "departure_time": datetime.now() + timedelta(days=10, hours=2),
        "arrival_time": datetime.now() + timedelta(days=10, hours=6),
        "status": FlightStatus.planned
    },
]


async def seed_flights():
    await seed_all(FlightBase, flight_data)