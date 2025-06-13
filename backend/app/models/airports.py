from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from backend.app.models.base import Base


class AirportBase(Base):

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    city: Mapped[str] = mapped_column(String(30), nullable=False)
    country: Mapped[str] = mapped_column(String(30), nullable=False)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    icao_code: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)
