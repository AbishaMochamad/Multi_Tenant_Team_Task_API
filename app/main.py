from typing import Annotated
from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.api import users_router
from app.db import get_db
from app.services import get_user, authenticate_user
from datetime import datetime, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from app.core import settings, create_access_token
from app.models import TokenData, Token, UserModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime, timedelta, timezone

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An expected error occured",
            "path": request.url.path,
            "timestamp": str(datetime.now(timezone.utc)),
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc.orig)})


@app.exception_handler(OperationalError)
async def database_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc.orig)})


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

@app.post("/token")
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
    return Token(access_token=access_token, token_type="bearer")

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}



@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> UserModel:
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users_router)
