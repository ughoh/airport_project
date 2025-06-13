from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AircraftBase(BaseModel):
    model: str = Field(max_length=50)
    capacity: int = Field(gt=0, lt=500)
    registration_number: int


class AircraftCreate(AircraftBase):
    pass


class AircraftUpdate(BaseModel):
    model: Optional[str] = None
    capacity: Optional[int] = None
    registration_number: Optional[int] = None


class Aircraft(AircraftBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
