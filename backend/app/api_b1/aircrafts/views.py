from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import db_helper
from . import crud
from .schemas import Aircraft, AircraftCreate, AircraftUpdate

router = APIRouter(tags=['Aircrafts'])


@router.get('/', response_model=list[Aircraft])
async def get_aircraft(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_aircrafts(session=session)


@router.post('/', response_model=Aircraft)
async def create_aircraft(aircraft: AircraftCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_aircraft(session=session, aircraft_create=aircraft)


@router.get('/{aircraft_id}/', response_model=Aircraft)
async def get_aircraft(aircraft_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    aircraft = await crud.read_aircraft(session=session, aircraft_id=aircraft_id)
    if aircraft is None:
        raise HTTPException(status_code=404, detail={'text': 'No aircraft found'})
    return aircraft


@router.delete('/delete/{aircraft_id}', response_model=Aircraft)
async def delete_aircraft(aircraft_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_aircraft(session=session, aircraft_id=aircraft_id)


@router.patch('/update/{aircraft_id}', response_model=Aircraft)
async def update_aircraft(aircraft_id: int, aircraft_update: AircraftUpdate,
                          session: AsyncSession = Depends(db_helper.session_dependency)):
    aircraft = await crud.read_aircraft(session, aircraft_id=aircraft_id)
    if aircraft is None:
        raise HTTPException(status_code=404, detail={'text': 'No aircraft found'})
    return await crud.update_aircraft(session=session, aircraft=aircraft, aircraft_update=aircraft_update)


@router.get('/get/param', response_model=list[Aircraft])
async def get_param(model: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    aircraft = await crud.get_aircraft(session=session, model=model)
    return aircraft
