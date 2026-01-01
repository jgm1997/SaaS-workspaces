from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn
    model_config = {
        "env_file": ".env",
        "extra": "allow",
    }


settings = Settings()
