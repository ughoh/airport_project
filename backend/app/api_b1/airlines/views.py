from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.models.db_helper import db_helper
from . import crud
from .schemas import Airline, AirlineCreate, AirlineUpdate

router = APIRouter(tags=['Airlines'])


@router.get('/', response_model=List[Airline])
async def get_airlines(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_airlines(session=session)


@router.post('/', response_model=Airline)
async def create_airline(airline: AirlineCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_airline(session=session, airline_create=airline)


@router.get('/{airline_id}/', response_model=Airline)
async def get_airline(airline_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    airline = await crud.read_airline(session=session, airline_id=airline_id)
    if airline is None:
        raise HTTPException(status_code=404, detail={'text': 'No airline found'})
    return airline


@router.delete('/delete/{airline_id}', response_model=Airline)
async def delete_airline(airline_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_airline(session=session, airline_id=airline_id)


@router.patch('/update/{airline_id}', response_model=Airline)
async def update_airline(airline_id: int, airline_update: AirlineUpdate,
                         session: AsyncSession = Depends(db_helper.session_dependency)):
    airline = await crud.read_airline(session, airline_id=airline_id)
    if airline is None:
        raise HTTPException(status_code=404, detail={'text': 'No airline found'})
    return await crud.update_airline(session=session, airline=airline, airline_update=airline_update)


@router.get('/get/by_name', response_model=List[Airline])
async def get_by_name(name: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    airlines = await crud.get_airline_by_name(session=session, name=name)
    return airlines
