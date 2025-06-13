from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.models.db_helper import db_helper
from . import crud
from .schemas import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(tags=["Employees"])


@router.get("/", response_model=List[Employee])
async def get_employees(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_employees(session=session)


@router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.create_employee(session=session, employee_create=employee)


@router.get("/{employee_id}/", response_model=Employee)
async def get_employee(employee_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    employee = await crud.read_employee(session=session, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail={"text": "No employee found"})
    return employee


@router.delete("/delete/{employee_id}", response_model=Employee)
async def delete_employee(employee_id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.delete_employee(session=session, employee_id=employee_id)


@router.patch("/update/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate,
                          session: AsyncSession = Depends(db_helper.session_dependency)):
    employee = await crud.read_employee(session=session, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail={"text": "No employee found"})
    return await crud.update_employee(session=session, employee=employee, employee_update=employee_update)


@router.get("/get/by_name", response_model=List[Employee])
async def get_by_departament(name: str, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_by_first_name(session=session, first_name=name)
