from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import User
from src.repository.likes import add_grade_to_image
from src.repository.likes import get_current_rating
from src.schemas.likes import ImageRating
from src.schemas.likes import LikeResponseSchema
from src.schemas.likes import LikeSchema
from src.services.auth import auth_service

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post(
    "/images/{image_id}/likes/{grade}",
    response_model=LikeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_grade_to_image_route(
    image_id: int,
    body: LikeSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Add grade to image.
    :param image_id: id of image
    :param body: schema with grade
    :param db: database session
    :param current_user: current user
    :return: grade of image
    """

    image_grade = await add_grade_to_image(image_id, body, db, current_user)
    return image_grade


@router.get(
    "/rating/{image_id}", response_model=ImageRating, status_code=status.HTTP_200_OK
)
async def get_image_rating(image_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get rating of image grade
    :param image_id: id of image
    :param db: database session
    :return: rating of image in JSON format
    """

    rating = await get_current_rating(image_id, db)
    return {
        "rating": rating,
        "image": image_id,
    }
