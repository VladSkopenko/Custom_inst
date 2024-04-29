
# from dotenv import load_dotenv
from os import environ
from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

# load_dotenv()
base_path_project = Path(__file__).resolve().parent.parent
base_path = base_path_project.parent
load_dotenv(base_path.joinpath(".env"))
APP_ENV = environ.get("APP_ENV")


class Settings(BaseSettings):
    APP_NAME: str = "myapp"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    SECRET_KEY_JWT: str = "secret_key"
    ALGORITHM: str = "HS256"

    DATABASE_HOST: str = 'localhost'
    DATABASE_USER: str = 'postgres'
    DATABASE_PASSWORD: str = 'postgres'
    DATABASE_NAME: str = 'postgres'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379

    CLOUDINARY_NAME: str = "dlfc34moq"
    CLOUDINARY_API_KEY: int = 287698145284357
    CLOUDINARY_API_SECRET: str = "FWrjBSc42NGO2k8YnrNYKOHIk5E"

    RATE_LIMITER_TIMES: int = 2
    RATE_LIMITER_SECONDS: int = 5
    STATIC_DIRECTORY: str = str(base_path_project.joinpath("static"))


    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()

