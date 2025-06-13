from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from backend.app.models.base import Base


class AirlineBase(Base):

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(String(30), nullable=False)
