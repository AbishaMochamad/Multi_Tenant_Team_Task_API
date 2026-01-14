from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: str


settings = Settings()
