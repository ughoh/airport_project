from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class BookingBase(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey("userbases.id"), nullable=False)
    outbound_id: Mapped[int] = mapped_column(ForeignKey("flightbases.id"), nullable=False)
    return_id: Mapped[int] = mapped_column(ForeignKey("flightbases.id"), nullable=True)
    sep_id: Mapped[int] = mapped_column(ForeignKey("flightbases.id"), nullable=True)
    sep_id_return: Mapped[int] = mapped_column(ForeignKey("flightbases.id"), nullable=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    passengers: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_class: Mapped[str] = mapped_column(String(20), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
