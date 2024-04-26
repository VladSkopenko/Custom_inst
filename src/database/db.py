import contextlib

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from src.conf.config import config

connection_string = URL.create(
    'postgresql',
    username=config.DATABASE_USER,
    password=config.DATABASE_PASSWORD,
    host=config.DATABASE_HOST,
    database=config.DATABASE_NAME,
)

engine = create_engine(connection_string)


class DataBaseSessionManager:
    def __init__(self, url: str):

        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session

        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DataBaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
