from typing import List, Type

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import AircraftBase
from .schemas import AircraftCreate, AircraftUpdate


async def get_aircrafts(session: AsyncSession) -> List[AircraftBase]:
    stmt = select(AircraftBase).order_by(AircraftBase.id)
    result: Result = await session.execute(stmt)
    results = result.scalars().all()
    return list(results)


async def read_aircraft(session: AsyncSession, aircraft_id: int) -> AircraftBase | None:
    return await session.get(AircraftBase, aircraft_id)


async def create_aircraft(session: AsyncSession, aircraft_create: AircraftCreate) -> AircraftBase:
    aircraft = AircraftBase(**aircraft_create.model_dump())
    session.add(aircraft)
    await session.commit()
    await session.refresh(aircraft)
    return aircraft


async def delete_aircraft(session: AsyncSession, aircraft_id: int) -> Type[AircraftBase]:
    result = await session.get(AircraftBase, aircraft_id)
    if not result:
        raise HTTPException(status_code=404, detail="Aircraft not found")

    await session.delete(result)
    await session.commit()
    return result


async def update_aircraft(session: AsyncSession, aircraft: AircraftBase, aircraft_update: AircraftUpdate) -> AircraftBase:
    for name, value in aircraft_update.model_dump(exclude_unset=True).items():
        setattr(aircraft, name, value)
    await session.commit()
    await session.refresh(aircraft)
    return aircraft


async def get_aircraft(session: AsyncSession, model: str) -> List[AircraftBase]:
    stmt = select(AircraftBase).where(AircraftBase.model == model).order_by(AircraftBase.id)
    result: Result = await session.execute(stmt)
    results = result.scalars().all()
    return list(results)


