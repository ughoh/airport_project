from backend.app.models import Seats, TicketBase
from seed_all import seed_all

ticket_data = [
    {
        "flight_id": 1,
        "passenger_id": 1,
        "seat_number": "12A",
        "seat_class": Seats.economy,
        "price": 150
    },
    {
        "flight_id": 2,
        "passenger_id": 2,
        "seat_number": "2B",
        "seat_class": Seats.business,
        "price": 420
    },
    {
        "flight_id": 3,
        "passenger_id": 3,
        "seat_number": "1A",
        "seat_class": Seats.first_class,
        "price": 890
    },
    {
        "flight_id": 4,
        "passenger_id": 4,
        "seat_number": "16C",
        "seat_class": Seats.economy,
        "price": 130
    },
    {
        "flight_id": 5,
        "passenger_id": 5,
        "seat_number": "3D",
        "seat_class": Seats.business,
        "price": 390
    },
    {
        "flight_id": 6,
        "passenger_id": 6,
        "seat_number": "4F",
        "seat_class": Seats.economy,
        "price": 160
    },
    {
        "flight_id": 7,
        "passenger_id": 7,
        "seat_number": "1C",
        "seat_class": Seats.first_class,
        "price": 950
    },
    {
        "flight_id": 8,
        "passenger_id": 8,
        "seat_number": "10E",
        "seat_class": Seats.economy,
        "price": 140
    },
    {
        "flight_id": 9,
        "passenger_id": 9,
        "seat_number": "2A",
        "seat_class": Seats.business,
        "price": 400
    },
    {
        "flight_id": 10,
        "passenger_id": 10,
        "seat_number": "14B",
        "seat_class": Seats.economy,
        "price": 120
    },
]


async def seed_tickets():
    await seed_all(TicketBase, ticket_data)
