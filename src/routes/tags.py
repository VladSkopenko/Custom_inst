from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import User
from src.repository.tags import create_tag
from src.repository.tags import delete_tag
from src.repository.tags import get_tag
from src.schemas.tags import TagSchema
from src.schemas.tags import TagTypeChoices
from src.services.auth import auth_service
from src.repository.tags import add_tag_to_image
router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/tag_types")
async def show_types():
    return [tag_type.value for tag_type in TagTypeChoices]


@router.get("/{tag_id}/", response_model=TagSchema)
async def get_tag_router(tag_name, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user), ):
    tag = await get_tag(tag_name, db, current_user)
    return tag


@router.post(
    "/create_tag", response_model=TagSchema, status_code=status.HTTP_201_CREATED
)
async def create_tag_router(
        body: TagSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    tag = await create_tag(body, db, current_user)
    if not tag:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return tag


@router.delete("/delete/{comment_id}/", response_model=TagSchema)
async def delete_tag_route(
        tag_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    tag = await delete_tag(tag_id, db, current_user)
    return tag


@router.post("/images/{image_id}/tags/{tag_name}", status_code=201)
async def add_tag_to_image_route(
    image_id: int,
    tag_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    try:
        await add_tag_to_image(image_id, tag_name, db, current_user)
        return {"message": detail_message.ADD_TAG_SUCCESS}
    except HTTPException as e:
        return e
