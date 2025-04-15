from __future__ import annotations

import os
from abc import abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


class IAuth:
    """
    Interface for authentication and password hashing.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash the password using bcrypt.
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify the password against the hashed password.
        """
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Create an access token with an expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def get_password_hash(password) -> str:
        return PWD_CONTEXT.hash(password)

    @staticmethod
    def get_expire_minutes():
        """
        Get the expiration time in minutes for the access token.
        """
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    async def get_current_user(self, token: Annotated[str, Depends(OAUTH2_SCHEME)]):
        from models.user import TokenData, UserDetail  # noqa: F401

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        current_user: Annotated[UserDetail, Depends(get_current_user)],
    ):
        from models.user import UserDetail  # noqa: F401

        return current_user

    @classmethod
    @abstractmethod
    def get_by_username(cls, username: str) -> UserDetail | None:
        """
        Get user by username.
        """
        from models.user import UserDetail  # noqa: F401

        pass
