from pydantic import BaseModel
from enum import Enum


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    departament: str
    contact_info: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    position: str
    departament: str
    contact_info: str


class Employee(EmployeeBase):
    id: int
