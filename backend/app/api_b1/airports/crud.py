from typing import List, Type
from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import AirportBase
from .schemas import AirportCreate, AirportUpdate


async def get_airports(session: AsyncSession) -> List[AirportBase]:
    stmt = select(AirportBase).order_by(AirportBase.id)
    result: Result = await session.execute(stmt)
    airports = result.scalars().all()
    return list(airports)


async def read_airport(session: AsyncSession, airport_id: int) -> AirportBase | None:
    return await session.get(AirportBase, airport_id)


async def create_airport(session: AsyncSession, airport_create: AirportCreate) -> AirportBase:
    airport = AirportBase(**airport_create.model_dump())
    session.add(airport)
    await session.commit()
    await session.refresh(airport)
    return airport


async def delete_airport(session: AsyncSession, airport_id: int) -> Type[AirportBase]:
    airport = await session.get(AirportBase, airport_id)
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    await session.delete(airport)
    await session.commit()
    return airport


async def update_airport(session: AsyncSession, airport: AirportBase, airport_update: AirportUpdate) -> AirportBase:
    for name, value in airport_update.model_dump(exclude_unset=True).items():
        setattr(airport, name, value)
    await session.commit()
    await session.refresh(airport)
    return airport


async def get_airport_by_iata(session: AsyncSession, iata_code: str) -> List[AirportBase]:
    stmt = select(AirportBase).where(AirportBase.iata_code == iata_code).order_by(AirportBase.id)
    result: Result = await session.execute(stmt)
    airports = result.scalars().all()
    return list(airports)

