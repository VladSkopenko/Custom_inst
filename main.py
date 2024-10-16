import os
import pathlib
import threading
import webbrowser
from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.conf.config import config
from src.database.db import check_redis
from src.database.db import get_redis
from src.routes import auth
from src.routes import comments
from src.routes import frontend
from src.routes import healthchecker_db
from src.routes import images
from src.routes import likes
from src.routes import tags
from src.routes import tags_images
from src.routes import users
from src.utils.logger import handler
from src.utils.logger import logger
from src.utils.staticfilescache import StaticFilesCache

logger.addHandler(handler)
static_files_path = os.path.join(os.path.dirname(__file__), "src", "static")

if not static_files_path:
    raise RuntimeError("STATIC_DIRECTORY does not exist")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The lifespan function is a context manager that runs during the lifespan of the application.

    :param app: FastAPI: Pass the FastAPI app
    :return: A lifespan function
    """

    logger.debug("lifespan before")
    try:
        await startup()
    except redis.ConnectionError as err:
        logger.error(f"redis err: {err}")
    except Exception as err:
        logger.error(f"other app err: {err}")
    yield
    logger.debug("lifespan after")


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(healthchecker_db.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(images.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(tags_images.router, prefix="/api")
app.include_router(likes.router, prefix="/api")
app.include_router(frontend.router)


async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    like database connections or external APIs.

    :return: A dictionary with a key called &quot;app&quot;
    :doc-author: Trelent
    """
    redi = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(redi)


async def get_limit():
    """
    The get_limit function.

    :return: None
    """

    return None


async def deny_get_redis():
    """
    The deny_get_redis function.

    :return: None
    """

    return None


static_dir: pathlib.Path = pathlib.Path(config.STATIC_DIRECTORY)
static_files_path = os.path.join(os.path.dirname(__file__), "src", "static")
if not static_files_path:
    raise RuntimeError("STATIC_DIRECTORY does not exist")


app.mount(
    path="/static",
    app=StaticFilesCache(
        directory=static_files_path, cachecontrol="private, max-age=3600"
    ),
    name="static",
)
app.mount(
    path="/sphinx",
    app=StaticFilesCache(directory=config.SPHINX_DIRECTORY, html=True),
    name="sphinx",
)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, timeout_keep_alive=120)
