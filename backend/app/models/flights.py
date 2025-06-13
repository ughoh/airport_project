from sqlalchemy import ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.base import Base
import enum


class FlightBase(Base):

    airline_id: Mapped[int] = mapped_column(ForeignKey('airlinebases.id'), nullable=False)
    flight_number: Mapped[str] = mapped_column(nullable=False)
    aircraft_id: Mapped[int] = mapped_column(ForeignKey('aircraftbases.id'), nullable=False)
    departure_airport_id: Mapped[int] = mapped_column(ForeignKey('airportbases.id'), nullable=False)
    arrival_airport_id: Mapped[int] = mapped_column(ForeignKey('airportbases.id'), nullable=False)
    departure_time: Mapped[datetime] = mapped_column(nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)