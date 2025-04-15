from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.user import Token, User, UserCreate, UserDetail

# from fastapi.responses import JSONResponse

blueprint_name = "auth"

router = APIRouter(
    prefix=f"/{blueprint_name}",
    tags=[blueprint_name],
    responses={404: {"description": "Not found"}},
)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = User.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=User.get_expire_minutes())
    access_token = User.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/registry")
async def create_user(user: UserCreate) -> UserDetail:
    """
    Create a new user.

    @JSON Params:\n
        - username: Username of the user\n
        - password: Password of the user\n
        - is_superuser: Is the user a superuser?\n

    @Return:\n
        - UserDetail: Details of the created user\n
            * username: Username of the user\n
            * is_superuser: Is the user a superuser?\n
    """
    db_user = User.get_by_username(user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    if not user.username or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )

    db_user = User(**user.model_dump())
    db_user.password = User.get_password_hash(user.password)
    db_user.create()
    return UserDetail(username=db_user.username, is_superuser=db_user.is_superuser)
