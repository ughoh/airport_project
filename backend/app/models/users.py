from sqlalchemy import Column, String
from backend.app.models.base import Base


class UserBase(Base):

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
