from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import User
from src.repository.tags_images import add_tag_to_image
from src.repository.tags_images import remove_tag_from_image
from src.services.auth import auth_service

router = APIRouter(prefix="/tags_images", tags=["tags_images"])


@router.post("/images/{image_id}/tags/{tag_name}", status_code=201)
async def add_tag_to_image_route(
    image_id: int,
    tag_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    await add_tag_to_image(image_id, tag_name, db, current_user)
    return {"message": detail_message.ADD_TAG_SUCCESS}


@router.delete("/images/{image_id}/tags/{tag_name}", status_code=200)
async def remove_tag_from_image_route(
    image_id: int,
    tag_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    await remove_tag_from_image(image_id, tag_name, db, current_user)
    return {"message": detail_message.REMOVE_TAG_SUCCESS}
