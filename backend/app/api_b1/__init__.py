from fastapi import APIRouter

from .aircrafts.views import router as aircrafts_router
from .airports.views import router as airport_router
from .flights.views import router as flight_router
from .users.views import router as user_router
from .airlines.views import router as airline_router
from .booking.views import router as booking_router
from .employees.views import router as employee_router

router = APIRouter()
router.include_router(router=aircrafts_router, prefix='/aircrafts')
router.include_router(router=airport_router, prefix='/airport')

router.include_router(router=flight_router, prefix='/flights')

router.include_router(router=user_router, prefix='/users')

router.include_router(router=booking_router, prefix='/booking')

router.include_router(router=airline_router, prefix='/airlines')

router.include_router(router=employee_router, prefix='/employees')
