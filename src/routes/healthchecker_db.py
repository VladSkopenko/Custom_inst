from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db

router = APIRouter(prefix="/healthchecker", tags=["healthchecker"])


@router.get("/")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks the health of the database.
    It does this by executing a SQL query and checking if it returns any results. If it doesn't,
    then we know something is wrong with our database connection.

    :param db: AsyncSession: Inject the database session into the function
    :return: A dictionary with a message
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail=detail_message.DATABASE_ERROR)
        return {"message": detail_message.GREETING}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=detail_message.CONNECT_DATABASE_ERROR
        )
