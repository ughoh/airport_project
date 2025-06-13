from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import db_helper
from . import crud

router = APIRouter(tags=['Flights'])


@router.get('/table')
async def get_table(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_flights_table(session=session)


@router.get('/chosen')
async def get_chosen(from_: str, to: str, dateGo: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.search_flights(from_city=from_, to_city=to, date=dateGo, session=session)


@router.get('/chosen_round')
async def get_chosen_round(from_: str, to: str, dateGo: str, dateReturn: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    oneWay = await crud.search_flights(from_city=from_, to_city=to, date=dateGo, session=session)
    wayBack = await crud.search_flights(from_city=to, to_city=from_, date=dateReturn, session=session)

    return {
        "outbound": oneWay,
        "return": wayBack
    }


@router.get('/flights/{flight_id}')
async def get_flight_by_id(flight_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    flight = await crud.get_flights_id(flight_id, session)
    if not flight:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.get('/flights_sep')
async def get_flights_sep(from_: str, to: str, dateGo, session: AsyncSession = Depends(db_helper.session_dependency)):
    res_one = await crud.get_flights_sep_first(from_city=from_, dateGO=dateGo, session=session)

    tickets_with_connection = []

    for first_flight in res_one:
        new_from = first_flight['to']
        new_date = first_flight['arrival_date']

        second_flights = await crud.get_flights_sep_second(
            from_city=new_from,
            to_city=to,
            dateGo=new_date,
            session=session
        )

        for second_flight in second_flights:
            tickets_with_connection.append({
                "first_leg": first_flight,
                "second_leg": second_flight
            })

    return tickets_with_connection


@router.get('/flights_sep_return')
async def get_chosen_round_full(
    from_: str,
    to: str,
    dateGo: str,
    dateReturn: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    direct_outbound = await crud.search_flights(from_city=from_, to_city=to, date=dateGo, session=session)
    direct_return = await crud.search_flights(from_city=to, to_city=from_, date=dateReturn, session=session)

    sep_outbound = await crud.get_sep_flight_pairs(from_, to, dateGo, session)
    sep_return = await crud.get_sep_flight_pairs(to, from_, dateReturn, session)

    return {
        "outbound": direct_outbound + [
            {
                "is_connection": True,
                "first_leg": pair["first_leg"],
                "second_leg": pair["second_leg"],
            }
            for pair in sep_outbound
        ],
        "return": direct_return + [
            {
                "is_connection": True,
                "first_leg": pair["first_leg"],
                "second_leg": pair["second_leg"],
            }
            for pair in sep_return
        ]
    }
