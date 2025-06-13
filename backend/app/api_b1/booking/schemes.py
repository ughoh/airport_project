from pydantic import BaseModel


class BookingRequestWithEmail(BaseModel):
    outbound_id: int
    return_id: int | None = None
    sep_id: int | None = None
    sep_id_return: int | None = None
    first_name: str
    last_name: str
    passengers: int
    ticket_class: str
    total_price: int
    user_email: str
