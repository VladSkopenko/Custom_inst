from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Role
from src.database.models import Tag
from src.database.models import User
from src.schemas.tags import TagSchema


async def get_tag(tag_name: str, db: AsyncSession, current_user: User):
    stmt = select(Tag).where(Tag.tag_name == tag_name)
    existing_tag = await db.execute(stmt)
    tag = existing_tag.scalar_one_or_none()
    if tag:
        return tag


async def create_tag(body: TagSchema, db: AsyncSession, current_user: User):
    tag = await get_tag(body.tag_name, db, current_user)
    if tag:
        return tag
    else:
        new_tag = Tag(tag_name=body.tag_name, tag_type=body.tag_type)
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)
        return new_tag


async def delete_tag(tag_id: int, db: AsyncSession, current_user: User):
    if current_user.role not in (Role.admin, Role.moderator):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail_message.PERMISSION_ERROR,
        )
    stmt = select(Tag).where(Tag.id == tag_id)
    existing_tag = await db.execute(stmt)
    tag = existing_tag.scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()
        return tag
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail_message.FILE_NOT_FOUND
        )