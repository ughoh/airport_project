from typing import List, Type
from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import EmployeesBase
from .schemas import EmployeeCreate, EmployeeUpdate


async def get_employees(session: AsyncSession) -> List[EmployeesBase]:
    stmt = select(EmployeesBase).order_by(EmployeesBase.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def read_employee(session: AsyncSession, employee_id: int) -> EmployeesBase | None:
    return await session.get(EmployeesBase, employee_id)


async def create_employee(session: AsyncSession, employee_create: EmployeeCreate) -> EmployeesBase:
    data = employee_create.model_dump()
    employee = EmployeesBase(**data)
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def delete_employee(session: AsyncSession, employee_id: int) -> Type[EmployeesBase]:
    employee = await session.get(EmployeesBase, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(employee)
    await session.commit()
    return employee


async def update_employee(session: AsyncSession, employee: EmployeesBase, employee_update: EmployeeUpdate) -> EmployeesBase:
    for name, value in employee_update.model_dump(exclude_unset=True).items():
        setattr(employee, name, value)
    await session.commit()
    await session.refresh(employee)
    return employee


async def get_by_first_name(session: AsyncSession, first_name: str) -> List[EmployeesBase]:
    stmt = select(EmployeesBase).where(EmployeesBase.first_name.ilike(f"%{first_name}%")).order_by(EmployeesBase.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()