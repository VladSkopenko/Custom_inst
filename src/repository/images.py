from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.images import ImageSchema
from src.database.models import Image
from src.database.models import User, Role


async def create_image(body: ImageSchema, base_url: str, db: AsyncSession, current_user: User):
    image = Image(**body.dict())
    if image.title is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")
    image.base_url = base_url
    image.user_id = current_user.id
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image(image_id: int, db: AsyncSession):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image:
        return image
    else:
        return None


async def update_image(image_id: int, body: ImageSchema, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image.user_id != current_user.id and current_user.role not in (Role.admin, Role.moderator):
        return None
    if image:
        image.title = body.title
        # image.transform_url = body.transform_url
        image.description = body.description
        # image.tags = body.tags
        # image.qr_url = body.qr_url
        await db.commit()
        await db.refresh(image)
        return image
    else:
        return None


async def delete_image(image_id: int, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image.user_id != current_user.id and current_user.role not in (Role.admin, Role.moderator):
        return None
    if image:
        await db.delete(image)
        await db.commit()
    return image
