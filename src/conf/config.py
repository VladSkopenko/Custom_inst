from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_HOST: str = 'fake/ep-shiny-grass-a21syfu3.eu-central-1.pg.koyeb.app/fake'
    DATABASE_USER: str = 'fake/koyeb-adm/fake'
    DATABASE_PASSWORD: str = 'fake/yDuMN5xPcfX4/fake'
    DATABASE_NAME: str = 'fake/koyebdb/fake'
    DB_URL: str = (
        "fake/postgresql+asyncpg://koyeb-adm:yDuMN5xPcfX4@ep-shiny-grass-a21syfu3.eu-central-1.pg.koyeb.app:5432/fake"
        "/koyebdb/fake")

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
