import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# def _get_int(name: str, default: int) -> int:
#     value = os.getenv(name)
#     return int(value) if value else default


@dataclass(frozen=True)
class Settings:
    postgres_user: str | None = os.getenv("POSTGRES_USER")
    postgres_password: str | None = os.getenv("POSTGRES_PASS")
    postgres_database: str | None = os.getenv("POSTGRES_NAME")
    postgres_host: str | None = os.getenv("POSTGRES_HOST")
    postgres_port: int | None = os.getenv("POSTGRES_PORT")

    redis_host: str | None = os.getenv("REDIS_HOST")
    redis_port: int | None = os.getenv("REDIS_PORT")
    redis_db: int | None = os.getenv("REDIS_DB")
    redis_password: str | None = os.getenv("REDIS_PASS")


settings = Settings()
