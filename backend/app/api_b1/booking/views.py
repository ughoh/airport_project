from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import BookingBase, UserBase, db_helper
from .schemes import BookingRequestWithEmail
from ..flights.crud import get_flights_id

router = APIRouter(tags=['Booking'])


@router.post("/bookings")
async def create_booking(
    booking_data: BookingRequestWithEmail,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    print("Booking data received:", booking_data)
    result = await session.execute(select(UserBase).where(UserBase.email == booking_data.user_email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_booking = BookingBase(
        user_id=user.id,
        outbound_id=booking_data.outbound_id,
        return_id=booking_data.return_id,
        sep_id=booking_data.sep_id,
        sep_id_return=booking_data.sep_id_return,
        first_name=booking_data.first_name,
        last_name=booking_data.last_name,
        passengers=booking_data.passengers,
        ticket_class=booking_data.ticket_class,
        total_price=booking_data.total_price,
    )

    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)

    return {"message": "Booking created", "booking_id": new_booking.id}


@router.get('/tickets')
async def get_tickets(
    email: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    stmt = (
        select(
            BookingBase.id,
            UserBase.email,
            BookingBase.passengers,
            BookingBase.first_name,
            BookingBase.last_name,
            BookingBase.ticket_class,
            BookingBase.total_price,
            BookingBase.outbound_id,
            BookingBase.sep_id,
            BookingBase.return_id,
            BookingBase.sep_id_return,
        )
        .join(UserBase, BookingBase.user_id == UserBase.id)
        .where(UserBase.email == email)
    )
    result = await session.execute(stmt)
    bookings = result.all()

    tickets = []
    for b in bookings:
        outbound = await get_flights_id(b.outbound_id, session)
        return_flight = await get_flights_id(b.return_id, session)
        sep = await get_flights_id(b.sep_id, session)
        sep_return = await get_flights_id(b.sep_id_return, session)

        tickets.append({
            "id": b.id,
            "email": b.email,
            "passengers": b.passengers,
            "first_name": b.first_name,
            "last_name": b.last_name,
            "ticket_class": b.ticket_class,
            "total_price": b.total_price,
            "outbound_flight": outbound,
            "sep_flight": sep,
            "return_flight": return_flight,
            "sep_flight_return": sep_return,
        })

    return tickets