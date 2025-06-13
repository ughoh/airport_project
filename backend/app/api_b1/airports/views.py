from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.models.db_helper import db_helper
from . import crud
from .schemas import Airport, AirportCreate, AirportUpdate

router = APIRouter(tags=['Airports'])


@router.get('/', response_model=List[Airport])
async def get_airports(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_airports(session=session)


@router.post('/', response_model=Airport)
async def create_airport(airport: AirportCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_airport(session=session, airport_create=airport)


@router.get('/{airport_id}/', response_model=Airport)
async def get_airport(airport_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    airport = await crud.read_airport(session=session, airport_id=airport_id)
    if airport is None:
        raise HTTPException(status_code=404, detail={'text': 'No airport found'})
    return airport


@router.delete('/delete/{airport_id}', response_model=Airport)
async def delete_airport(airport_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_airport(session=session, airport_id=airport_id)


@router.patch('/update/{airport_id}', response_model=Airport)
async def update_airport(airport_id: int, airport_update: AirportUpdate,
                         session: AsyncSession = Depends(db_helper.session_dependency)):
    airport = await crud.read_airport(session, airport_id=airport_id)
    if airport is None:
        raise HTTPException(status_code=404, detail={'text': 'No airport found'})
    return await crud.update_airport(session=session, airport=airport, airport_update=airport_update)


@router.get('/get/by_iata', response_model=List[Airport])
async def get_by_iata(iata_code: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    airports = await crud.get_airport_by_iata(session=session, iata_code=iata_code)
    return airports


