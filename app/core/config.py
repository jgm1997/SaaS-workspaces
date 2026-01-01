from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://saas:saas@localhost:5432/saas_db"

    class Config:
        env_file = ".env"


settings = Settings()
