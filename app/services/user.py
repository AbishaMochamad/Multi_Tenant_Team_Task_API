from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.core import settings, get_password_hash, verify_password, dummy_password
from app.db import Users
from app.models import CreateUserModel, UserModel

from pydantic import EmailStr, StringConstraints

from typing import Annotated


def fetch_users(db: Session) -> list[UserModel]:
    statement = select(Users)

    results = db.scalars(statement=statement).all()

    return [UserModel.model_validate(obj) for obj in results]


def add_user(db: Session, new_user: CreateUserModel) -> UserModel:
    hashed_password = get_password_hash(password=new_user.password.get_secret_value())

    statement = (
        insert(Users)
        .values(
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email,
            password=hashed_password,
            created_by=settings.db_user,
            updated_by=settings.db_user,
        )
        .returning(Users)
    )

    result = db.execute(statement=statement).scalar_one()

    db.commit()

    return UserModel.model_validate(result)


def get_user(db: Session, email: str | None):
    statement = select(Users).where(Users.email == email)
    user = db.execute(statement=statement).scalar_one_or_none()
    return user

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
