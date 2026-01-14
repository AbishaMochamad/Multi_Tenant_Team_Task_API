from ..core import settings
from sqlalchemy import URL, create_engine

url_connection = URL.create(
    "postgresql+pg8000",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    database=settings.db_name,
)

db_engine = create_engine(url=url_connection)
