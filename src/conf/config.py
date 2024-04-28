# from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# load_dotenv()


class Settings(BaseSettings):
    DATABASE_HOST: str = 'localhost'
    DATABASE_USER: str = 'postgres'
    DATABASE_PASSWORD: str = 'postgres'
    DATABASE_NAME: str = 'postgres'
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    CLD_NAME: str = "dlfc34moq"
    CLD_API_KEY: int = 287698145284357
    CLD_API_SECRET: str = "FWrjBSc42NGO2k8YnrNYKOHIk5E"

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
