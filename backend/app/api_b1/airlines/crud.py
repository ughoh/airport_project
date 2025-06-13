from typing import List, Type
from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import AirlineBase
from .schemas import AirlineCreate, AirlineUpdate


async def get_airlines(session: AsyncSession) -> List[AirlineBase]:
    stmt = select(AirlineBase).order_by(AirlineBase.id)
    result: Result = await session.execute(stmt)
    airlines = result.scalars().all()
    return list(airlines)


async def read_airline(session: AsyncSession, airline_id: int) -> AirlineBase | None:
    return await session.get(AirlineBase, airline_id)


async def create_airline(session: AsyncSession, airline_create: AirlineCreate) -> AirlineBase:
    airline = AirlineBase(**airline_create.model_dump())
    session.add(airline)
    await session.commit()
    await session.refresh(airline)
    return airline


async def delete_airline(session: AsyncSession, airline_id: int) -> Type[AirlineBase]:
    airline = await session.get(AirlineBase, airline_id)
    if not airline:
        raise HTTPException(status_code=404, detail="Airline not found")
    await session.delete(airline)
    await session.commit()
    return airline


async def update_airline(session: AsyncSession, airline: AirlineBase, airline_update: AirlineUpdate) -> AirlineBase:
    for name, value in airline_update.model_dump(exclude_unset=True).items():
        setattr(airline, name, value)
    await session.commit()
    await session.refresh(airline)
    return airline


async def get_airline_by_name(session: AsyncSession, name: str) -> List[AirlineBase]:
    stmt = select(AirlineBase).where(AirlineBase.name == name).order_by(AirlineBase.id)
    result: Result = await session.execute(stmt)
    airlines = result.scalars().all()
    return list(airlines)
