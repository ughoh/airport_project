from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from backend.app.models.base import Base


class AircraftBase(Base):

    model: Mapped[str] = mapped_column(String(30), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    registration_number: Mapped[int] = mapped_column(nullable=False)