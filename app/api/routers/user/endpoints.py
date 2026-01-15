from fastapi import APIRouter, Depends
from app.db import get_db
from sqlalchemy.orm import Session
from app.services import fetch_users
from app.models import User

users_router = APIRouter()


@users_router.get("/users")
def get_users(db: Session = Depends(get_db)) -> list[User]:
    return fetch_users(db=db)
