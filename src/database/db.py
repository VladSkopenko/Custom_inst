import contextlib
import logging

import redis.asyncio as redis
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from src.conf.config import config

logger = logging.getLogger(f"{config.APP_NAME}.{__name__}")


connection_string = URL.create(
    "postgresql",
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


def create_redis():
    return redis.ConnectionPool(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        decode_responses=False,
    )


def get_redis() -> redis.Redis | None:
    # Here, we re-use our connection pool
    # not creating a new one
    try:
        logger.debug("get_redis connection_pool")
        if redis_pool:
            connection = redis.Redis(connection_pool=redis_pool)
            return connection
        logger.debug("get_redis connection_pool None")
    except:
        logger.debug("get_redis except")


async def check_redis() -> bool | None:
    try:
        logger.debug("check_redis")
        r: redis.Redis | None = get_redis()
        if r:
            return await r.ping()
    except Exception:
        logger.debug("check_redis fail")
        return None


redis_pool: redis.ConnectionPool = create_redis()
