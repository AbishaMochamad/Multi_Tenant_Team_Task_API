from datetime import timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core import settings
from app.core.utilities.utilities import create_access_token
from app.db import get_db
from app.models import LoginRequest, RegisterRequest, CreateUserModel, UserModel, UserModelWithAccessToken
from app.models.commons.token import Token
from app.services import add_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services.authentication import authenticate_user

authentication_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@authentication_router.post("/register")
def register(register_form: RegisterRequest, db: Session = Depends(get_db)) -> UserModel:
    return add_user(
        db=db,
        new_user=CreateUserModel(
            first_name=register_form.first_name,
            email=register_form.email,
            last_name=register_form.last_name,
            password=register_form.password,
        )
    )


@authentication_router.post("/login")
def login(login_form: LoginRequest, db: Session = Depends(get_db)) -> UserModelWithAccessToken:
    user = authenticate_user(db=db, email=login_form.email, password=login_form.password.get_secret_value())

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return UserModelWithAccessToken(
        user=UserModel.model_validate(user),
        token=Token(access_token=access_token)
    )    


@authentication_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)