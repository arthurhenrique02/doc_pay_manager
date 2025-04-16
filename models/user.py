import os

from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .auth import IAuth
from .base import Base

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserDetail(BaseModel):
    id: int | None = None
    username: str
    is_superuser: bool | None = None


class UserInDB(UserDetail):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
    is_superuser: bool = False


class User(Base, IAuth):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    doctor = relationship("Doctor", back_populates="user")

    @classmethod
    def authenticate_user(cls, username: str, password: str) -> UserInDB | bool:
        user: UserInDB | bool = cls.get_by_username(username)

        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False

        return user

    @classmethod
    def get_by_username(cls, username: str) -> UserInDB | bool:
        user: User | None = cls.filter(username=username).first()

        if not user:
            return False

        return UserInDB(
            id=user.id,
            username=user.username,
            is_superuser=user.is_superuser,
            hashed_password=user.password,
        )
