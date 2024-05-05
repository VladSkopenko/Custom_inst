from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import Role
from src.database.models import User
from src.repository.tags import create_tag
from src.repository.tags import delete_tag
from src.repository.tags import get_tag
from src.schemas.tags import TagResponseSchema
from src.schemas.tags import TagSchema
from src.schemas.tags import TagTypeChoices
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/tags", tags=["tags"])

access_to_route_delete = RoleAccess([Role.admin, Role.moderator])


@router.get("/tag_types")
async def show_types():
    """
    Return list of tag types.

    :return: List of tag types
    """

    return [tag_type.value for tag_type in TagTypeChoices]


@router.get("/{tag_id}", response_model=TagResponseSchema)
async def get_tag_router(
    tag_name,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Get tag by name.

    :param tag_name: str: Name of the tag
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: Tag object in JSON format
    """

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
    """
    Create tag.

    :param body: TagSchema: Pass the tag data
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: Tag object in JSON format
    """

    tag = await create_tag(body, db, current_user)
    if not tag:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return tag


@router.delete(
    "/delete/{tag_id}",
    response_model=TagSchema,
    dependencies=[Depends(access_to_route_delete)],
)
async def delete_tag_route(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Delete tag.

    :param tag_id: int: Specify the tag id
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: Tag object in JSON format
    """

    tag = await delete_tag(tag_id, db, current_user)
    return tag
