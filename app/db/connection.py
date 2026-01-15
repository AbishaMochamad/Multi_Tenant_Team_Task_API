from ..core import settings
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

url_connection = URL.create(
    "postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    database=settings.db_name,
)

db_engine = create_engine(url=url_connection)
SessionLocal = sessionmaker(bind=db_engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
