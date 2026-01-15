from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Users
from app.models import User


def fetch_users(db: Session) -> list[User]:
    statement = select(Users)

    results = db.scalars(statement=statement).all()

    return [User.model_validate(obj) for obj in results]
