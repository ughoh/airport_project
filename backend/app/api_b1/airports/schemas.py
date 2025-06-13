from pydantic import BaseModel


class AirportBase(BaseModel):
    name: str
    city: str
    country: str
    iata_code: str
    icao_code: str


class AirportCreate(AirportBase):
    pass


class AirportUpdate(BaseModel):
    name: str
    city: str
    country: str
    iata_code: str
    icao_code: str


class Airport(AirportBase):
    id: int