from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.core import settings
from app.db import Users
from app.models import CreateUserModel, UserModel
from argon2 import PasswordHasher

ph = PasswordHasher()


def fetch_users(db: Session) -> list[UserModel]:
    statement = select(Users)

    results = db.scalars(statement=statement).all()

    return [UserModel.model_validate(obj) for obj in results]


def add_user(db: Session, new_user: CreateUserModel) -> UserModel:
    hashed_password = ph.hash(password=new_user.password.get_secret_value())

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
