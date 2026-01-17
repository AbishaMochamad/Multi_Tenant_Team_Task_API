from fastapi import APIRouter, Depends
from app.db import get_db
from sqlalchemy.orm import Session
from app.services import fetch_users, add_user
from app.models import CreateUserModel, UserModel

users_router = APIRouter()


@users_router.get("/users")
def get_users(db: Session = Depends(get_db)) -> list[UserModel]:
    return fetch_users(db=db)


@users_router.post("/user")
def create_user(new_user: CreateUserModel, db: Session = Depends(get_db)):
    return add_user(db=db, new_user=new_user)
