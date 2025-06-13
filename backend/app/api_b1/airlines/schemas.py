from pydantic import BaseModel


class AirlineBase(BaseModel):
    name: str
    code: int
    country: str


class AirlineCreate(AirlineBase):
    pass


class AirlineUpdate(BaseModel):
    name: str
    code: int
    country: str


class Airline(AirlineBase):
    id: int
