from pathlib import Path

import uvicorn
from fastapi import FastAPI

from src.routes import healthchecker_db, images

app = FastAPI()
app.include_router(healthchecker_db.router, prefix="/api")
app.include_router(images.router, prefix="/api")
BASE_DIR = Path(__file__).parent

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
    )
