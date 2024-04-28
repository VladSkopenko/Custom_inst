import logging
import threading
import time
import os
import webbrowser
import typing
import colorlog
import pathlib
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Path,
    Query,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from contextlib import asynccontextmanager
import uvicorn
from src.routes import auth

from sqlalchemy import text
from sqlalchemy.orm import Session
from src.routes import healthchecker_db, images_admin
from src.conf.config import config
from src.database.db import get_db, get_redis, check_redis

logger = logging.getLogger(f"{config.APP_NAME}")
logger.setLevel(logging.INFO)
handler = colorlog.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(yellow)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
)
logger.addHandler(handler)

templates_path = os.path.join(os.path.dirname(__file__), "src", "templates")
if not templates_path:
    raise RuntimeError("TEMPLATES_DIRECTORY does not exist")
templates = Jinja2Templates(directory=templates_path)


static_files_path = os.path.join(os.path.dirname(__file__), "src", "static")

if not static_files_path:
    raise RuntimeError("STATIC_DIRECTORY does not exist")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("lifespan before")
    try:
        await startup()
    except redis.ConnectionError as err:
        logger.error(f"redis err: {err}")
    except Exception as err:
        logger.error(f"other app err: {err}")
    yield
    logger.debug("lifespan after")


# lifespan = None
# redis_pool = False


app = FastAPI(lifespan=lifespan)

app.include_router(healthchecker_db.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(images_admin.router, prefix="/api")

# @app.on_event("startup")
async def startup():
    redis_live: bool | None = await check_redis()
    if not redis_live:
        # db.redis_pool = False
        app.dependency_overrides[get_redis] = deny_get_redis
        logger.debug("startup DISABLE REDIS THAT DOWN")
    else:
        await FastAPILimiter.init(get_redis())
        app.dependency_overrides[get_limit] = RateLimiter(
            times=config.RATE_LIMITER_TIMES, seconds=config.RATE_LIMITER_SECONDS
        )
        logger.debug("startup done")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_limit():
    return None


async def deny_get_redis():
    return None

static_dir: pathlib.Path = pathlib.Path(config.STATIC_DIRECTORY)


class StaticFilesCache(StaticFiles):
    def __init__(
        self,
        *args,
        cachecontrol="public, max-age=31536000, s-maxage=31536000, immutable",
        **kwargs,
    ):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp


static_files_path = os.path.join(os.path.dirname(__file__), "src", "static")
# print(f"{static_files_path=}")
if not static_files_path:
    raise RuntimeError("STATIC_DIRECTORY does not exist")


app.mount(
    path="/static",
    app=StaticFilesCache(
        directory=static_files_path, cachecontrol="private, max-age=3600"
    ),
    name="static",
)
# app.mount(
#     path="/sphinx",
#     app=StaticFilesCache(directory=config.SPHINX_DIRECTORY, html=True),
#     name="sphinx",
# )
# # print(f"{config.SPHINX_DIRECTORY=}")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    """
    Route to render the home page.
    This route renders the index.html template as the home page.
    Parameters:
    - request (Request): The incoming request object.
    Returns:
    - HTMLResponse: HTML response containing the rendered template.
    """
    try:
        context = {"request": request, "title": "Home Page"}
        # context = {
        #     "request": request,
        #     "title": f"{config.app_version.upper()} APP {config.app_name.upper()}",
        # }
        return templates.TemplateResponse("index.html", context)

    except Exception as e:
        print(f"Error rendering template: {e}")
        raise

# app.include_router(auth.router, prefix="/auth")
# app.include_router(users.router, prefix="/")


# Function to open the web browser
def open_browser():
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    # Start the web browser in a separate thread
    threading.Thread(target=open_browser).start()
    # Run the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)