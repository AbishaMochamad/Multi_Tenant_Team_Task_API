from typing import Annotated
from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from app.api import users_router, authentication_router
from datetime import datetime, timezone
from app.models import UserModel
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime, timedelta, timezone

from app.services.authentication import get_current_active_user

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
app.include_router(authentication_router)