#from dotenv import load_dotenv
from os import environ
from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

BASE_PATH_PROJECT = Path(__file__).resolve().parent.parent
# print(f"{BASE_PATH_PROJECT=}")
BASE_PATH = BASE_PATH_PROJECT.parent
# print(f"{BASE_PATH=}")
load_dotenv(BASE_PATH.joinpath(".env"))
APP_ENV = environ.get("APP_ENV")
# print(f"{APP_ENV=}")


class Settings(BaseSettings):
    APP_NAME: str = "myapp"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    DATABASE_HOST: str = 'localhost'
    DATABASE_USER: str = 'postgres'
    DATABASE_PASSWORD: str = 'postgres'
    DATABASE_NAME: str = 'postgres'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    REDIS_DOMAIN: str = "0.0.0.0"
    REDIS_PORT: int = 6379

    CLOUDINARY_NAME: str = "some_name"
    CLOUDINARY_API_KEY: str = "0000000000000"
    CLOUDINARY_API_SECRET: str = "some_secret"

    rate_limiter_times: int = 2
    rate_limiter_seconds: int = 5
    STATIC_DIRECTORY: str = str(BASE_PATH_PROJECT.joinpath("static"))
    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
