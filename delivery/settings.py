from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings, PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = {
        "postgresql",
        "postgresql+aiopg",
        "postgres",
    }


class Settings(BaseSettings):
    # SERVICE
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False

    # DB
    DB_URL: AsyncPostgresDsn


settings = Settings()
templates = Jinja2Templates(directory="templates")
