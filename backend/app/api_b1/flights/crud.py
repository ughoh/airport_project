from datetime import datetime, timedelta

from sqlalchemy.orm import aliased

from backend.app.models import FlightBase, AirportBase, AircraftBase, AirlineBase
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


now = datetime.now()
start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
end_of_day = start_of_day + timedelta(days=1)

async def get_flights_table(session: AsyncSession):
    departure_airport = aliased(AirportBase)
    arrival_airport = aliased(AirportBase)

    stmt = (select(FlightBase.id,
                   FlightBase.flight_number,
                  departure_airport.city,
                  arrival_airport.city,
                  FlightBase.departure_time,
                  FlightBase.arrival_time,
                  FlightBase.status)
            .join(departure_airport, departure_airport.id == FlightBase.departure_airport_id)
            .join(arrival_airport, arrival_airport.id == FlightBase.arrival_airport_id)
            .where(
                and_(
                    FlightBase.departure_time >= start_of_day,
                    FlightBase.departure_time < end_of_day,
                )
            )
    )
    result = await session.execute(stmt)
    row = result.fetchall()

    return [
        {
            "flight_id": flight_id,
            'flight_number': flight_number,
            "departure_airport_name": departure_airport,
            "arrival_airport_name": arrival_airport,
            "departure_time": departure_time.strftime("%d.%m.%Y %H:%M"),
            "arrival_time": arrival_time.strftime("%d.%m.%Y %H:%M"),
            "flight_status": flight_status
        }
        for flight_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, flight_status in row
    ]


async def search_flights(from_city: str, to_city: str, date: str, session: AsyncSession):
    departure_from = aliased(AirportBase)
    arrival_to = aliased(AirportBase)

    From_city = from_city.split('(')[0].strip()
    To_city = to_city.split('(')[0].strip()

    date_start = datetime.strptime(date, '%Y-%m-%d')
    date_end = date_start + timedelta(days=1)

    stmt = (
        select(
            FlightBase.id,
            departure_from.city,
            departure_from.name,
            arrival_to.city,
            arrival_to.name,
            FlightBase.departure_time,
            FlightBase.arrival_time,
            FlightBase.price
        )
        .join(departure_from, departure_from.id == FlightBase.departure_airport_id)
        .join(arrival_to, arrival_to.id == FlightBase.arrival_airport_id)
        .where(
            departure_from.city == From_city,
            arrival_to.city == To_city,
            FlightBase.departure_time >= date_start,
            FlightBase.departure_time < date_end
        )
    )

    result = await session.execute(stmt)
    rows = result.fetchall()

    return [
        {
            'id': flight_id,
            'from': from_city,
            'departure_airport': departure_from_name,
            'to': to_city,
            'arrival_airport': arrival_to_name,
            "departure_date": departure_time.strftime("%d.%m.%Y"),
            'departure_hours': departure_time.strftime('%H:%M'),
            "arrival_date": arrival_time.strftime("%d.%m.%Y"),
            "arrival_hours": arrival_time.strftime('%H:%M'),
            'flight_duration': _format_duration(arrival_time - departure_time),
            'price': price
        }
        for flight_id, from_city, departure_from_name, to_city, arrival_to_name, departure_time, arrival_time, price in rows
    ]


def _format_duration(td: timedelta) -> str:
    total_minutes = int(td.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m"


async def get_flights_id(id: int, session: AsyncSession):
    departure_airport = aliased(AirportBase)
    arrival_airport = aliased(AirportBase)

    stmt = (select(FlightBase.id,
                   FlightBase.flight_number,
                   AircraftBase.registration_number,
                   AirlineBase.name,
                  departure_airport.city,
                  arrival_airport.city,
                  FlightBase.departure_time,
                  FlightBase.arrival_time)
            .join(departure_airport, departure_airport.id == FlightBase.departure_airport_id)
            .join(arrival_airport, arrival_airport.id == FlightBase.arrival_airport_id)
            .join(AircraftBase, FlightBase.aircraft_id == AircraftBase.id)
            .join(AirlineBase, FlightBase.airline_id == AirlineBase.id)
            .where(FlightBase.id == id)
    )

    row = await session.execute(stmt)
    result = row.one_or_none()

    if not result:
        return None

    (
        flight_id,
        flight_number,
        aircraft,
        airline,
        departure_city,
        arrival_city,
        departure_time,
        arrival_time
    ) = result

    return {
        "flight_id": flight_id,
        "flight_number": flight_number,
        "departure_city": departure_city,
        "arrival_city": arrival_city,
        "departure_time": departure_time.strftime("%d.%m.%Y %H:%M"),
        "arrival_time": arrival_time.strftime("%d.%m.%Y %H:%M"),
        "aircraft": aircraft,
        "airline": airline
    }


async def get_flights_sep_first(from_city: str, dateGO: str, session: AsyncSession):

    From_city = from_city.split('(')[0].strip()

    departure_from = aliased(AirportBase)
    arrival_to = aliased(AirportBase)

    date_start = datetime.strptime(dateGO, '%Y-%m-%d')
    date_end = date_start + timedelta(days=1)

    stmt = ((select(FlightBase.id,
                    departure_from.city,
                    departure_from.name,
                    arrival_to.city,
                    arrival_to.name,
                    FlightBase.departure_time,
                    FlightBase.arrival_time,
                    FlightBase.price
                   )
            .join(departure_from, departure_from.id == FlightBase.departure_airport_id)
            .join(arrival_to, arrival_to.id == FlightBase.arrival_airport_id)
            .where(departure_from.city == From_city,
                   FlightBase.departure_time >= date_start,
                   FlightBase.departure_time < date_end)))

    row = await session.execute(stmt)
    rows = row.fetchall()

    return [
        {
            'id': flight_id,
            'from': from_city,
            'departure_airport': departure_from_name,
            'to': to_city,
            'arrival_airport': arrival_to_name,
            "departure_date": departure_time.strftime("%d.%m.%Y"),
            'departure_hours': departure_time.strftime('%H:%M'),
            "arrival_date": arrival_time.strftime("%d.%m.%Y"),
            "arrival_hours": arrival_time.strftime('%H:%M'),
            'flight_duration': _format_duration(arrival_time - departure_time),
            'price': price
        }
        for flight_id, from_city, departure_from_name, to_city, arrival_to_name, departure_time, arrival_time, price in rows
    ]


async def get_flights_sep_second(from_city: str, to_city: str, dateGo, session: AsyncSession):
    departure_from = aliased(AirportBase)
    arrival_to = aliased(AirportBase)

    From_city = from_city.split('(')[0].strip()
    To_city = to_city.split('(')[0].strip()

    date_start = datetime.strptime(dateGo, "%d.%m.%Y") + timedelta(days=1)
    date_end = date_start + timedelta(days=2)

    stmt = ((select(FlightBase.id,
                    departure_from.city,
                    departure_from.name,
                    arrival_to.city,
                    arrival_to.name,
                    FlightBase.departure_time,
                    FlightBase.arrival_time,
                    FlightBase.price
                    )
             .join(departure_from, departure_from.id == FlightBase.departure_airport_id)
             .join(arrival_to, arrival_to.id == FlightBase.arrival_airport_id)
             .where(departure_from.city == From_city,
                    arrival_to.city == To_city,
                    FlightBase.departure_time > date_start,
                    FlightBase.departure_time < date_end)))

    row = await session.execute(stmt)
    rows = row.fetchall()

    return [
        {
            'id': flight_id,
            'from': from_city,
            'departure_airport': departure_from_name,
            'to': to_city,
            'arrival_airport': arrival_to_name,
            "departure_date": departure_time.strftime("%d.%m.%Y"),
            'departure_hours': departure_time.strftime('%H:%M'),
            "arrival_date": arrival_time.strftime("%d.%m.%Y"),
            "arrival_hours": arrival_time.strftime('%H:%M'),
            'flight_duration': _format_duration(arrival_time - departure_time),
            'price': price
        }
        for flight_id, from_city, departure_from_name, to_city, arrival_to_name, departure_time, arrival_time, price in
        rows
    ]


async def get_sep_flight_pairs(from_city: str, to_city: str, dateGo: str, session: AsyncSession):
    first_legs = await get_flights_sep_first(from_city, dateGo, session)
    result = []

    for first in first_legs:
        second_legs = await get_flights_sep_second(
            from_city=first["to"],
            to_city=to_city,
            dateGo=first["arrival_date"],
            session=session,
        )
        for second in second_legs:
            result.append({
                "first_leg": first,
                "second_leg": second,
            })

    return result
