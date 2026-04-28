from pydantic import EmailStr, StringConstraints

from app.core import settings, verify_password, dummy_password
from app.core.utilities.utilities import verify_password
from app.db import get_db
from app.models.user_model import UserModel
from app.services import get_user

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session
from typing import Annotated

from app.models.commons.token import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    return current_user


def authenticate_user(
    db: Session,
    email: Annotated[EmailStr, StringConstraints(max_length=50)],
    password: str,
):
    user = get_user(db=db, email=email)

    if not user:
        verify_password(plain_password=password, hashed_password=dummy_password)
        return None
    if not verify_password(plain_password=password, hashed_password=user.password):
        return None

    return user
