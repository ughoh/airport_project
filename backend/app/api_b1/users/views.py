from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.models import UserBase
from .schemas import UserCreate
from backend.app.models import db_helper
from backend.app.security import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.security import verify_password, create_access_token
from sqlalchemy import select

router = APIRouter()


@router.post("/register")
async def register(user_create: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    result = await session.execute(select(UserBase).where(UserBase.email == user_create.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    result_count = await session.execute(select(func.count()).select_from(UserBase))
    is_first_user = result_count.scalar_one() == 0
    role = "admin" if is_first_user else "user"

    hashed_pw = hash_password(user_create.password)
    new_user = UserBase(email=user_create.email, hashed_password=hashed_pw, role=role)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"message": f"User {new_user.email} registered as {new_user.role}"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.session_dependency)):
    result = await session.execute(select(UserBase).where(UserBase.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.email), "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}