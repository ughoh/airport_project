import asyncio
from seed_aircraft import seed_aircraft
from seed_flights import seed_flights
from seed_airports import seed_airports
from seed_airlines import seed_airlines
from seed_employees import seed_employees
from seed_passengers import seed_passengers
from seed_tickets import seed_tickets


async def seed_func():
    await seed_aircraft()
    await seed_airlines()
    await seed_airports()
    await seed_employees()
    await seed_passengers()
    await seed_flights()
    await seed_tickets()


asyncio.run(seed_func())