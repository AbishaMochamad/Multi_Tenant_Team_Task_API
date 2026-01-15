from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_name: str
    db_host: str
    db_user: str
    db_password: str
    db_port: str


settings = Settings()
