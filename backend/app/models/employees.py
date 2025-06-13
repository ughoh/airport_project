from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from backend.app.models.base import Base


class EmployeesBase(Base):

    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    position: Mapped[str] = mapped_column(String(30), nullable=False)
    departament: Mapped[str] = mapped_column(String(30), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(20), nullable=False)
