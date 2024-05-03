from fastapi import HTTPException
from fastapi import status
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import image_m2m_tag
from src.database.models import User
from src.repository.comments import get_comments_by_image
from src.repository.images import get_image
from src.repository.likes import get_current_rating
from src.repository.tags import create_tag, get_tag
from src.schemas.tags import TagSchema


async def add_tag_to_image(
    image_id: int, body: TagSchema, db: AsyncSession, current_user: User
):
    image = await get_image(image_id, db)
    owner_image = image.user_id
    if owner_image != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail_message.PERMISSION_ERROR,
        )
    tag = await create_tag(body, db, current_user)
    stmt = select(func.count(image_m2m_tag.c.tag_id)).where(
        image_m2m_tag.c.image_id == image_id
    )
    result = await db.execute(stmt)
    tag_count = result.scalar()
    if tag_count >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_message.LIMIT_TAG
        )
    elif image and tag:
        stmt = image_m2m_tag.insert().values(image_id=image_id, tag_id=tag.id)
        await db.execute(stmt)
        await db.commit()
        return detail_message.ADD_TAG_SUCCESS
    else:
        return detail_message.FILE_NOT_FOUND


async def remove_tag_from_image(
    image_id: int, tag_name: str, db: AsyncSession, current_user: User
):
    image = await get_image(image_id, db)
    owner_image = image.user_id
    if owner_image != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail_message.PERMISSION_ERROR,
        )
    tag = await get_tag(tag_name, db, current_user)
    if image and tag:
        stmt = image_m2m_tag.delete().where(
            image_m2m_tag.c.image_id == image_id, image_m2m_tag.c.tag_id == tag.id
        )
        await db.execute(stmt)
        await db.commit()
        return detail_message.REMOVE_TAG_SUCCESS
    else:
        return detail_message.FILE_NOT_FOUND


async def get_tags_by_image(image_id: int, db: AsyncSession):
    stmt = select(image_m2m_tag.c.tag_id).where(image_m2m_tag.c.image_id == image_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_data_image(image_id: int, db: AsyncSession):
    image = await get_image(image_id, db)
    comments = await get_comments_by_image(image_id, db)
    tags = await get_tags_by_image(image_id, db)
    rating = await get_current_rating(image_id, db)
    data_image = {
        "image": image,
        "tags_id": tags,
        "comments_info": comments,
        "rating": rating,
    }
    return data_image
