from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Image
from src.database.models import User, Role
from src.schemas.images import ImageSchema


async def create_image(
    body: ImageSchema, base_url: str, db: AsyncSession, current_user: User
):
    image = Image(**body.dict())
    if image.title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required"
        )
    image.base_url = base_url
    image.transform_url = base_url
    image.user_id = current_user.id
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image(image_id: int, db: AsyncSession, mode=1):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image is None:
        return None
    if mode == 1:
        image_dict = {
            "id": image.id,
            "user_id": image.user_id,
            "title": image.title,
            "base_url": image.base_url,
            "transform_url": image.transform_url,
            "description": image.description,
            "qr_url": image.qr_url,
            "created_at": image.created_at,
            "updated_at": image.updated_at,
            "user": {"id": image.user_id,
                     "nickname": image.user.nickname,
                     "created_at": image.user.created_at,
                     "role": image.user.role
                     }
            ,
        }
        return image_dict
    else:
        return image


async def update_image(
    image_id: int, body: ImageSchema, db: AsyncSession, current_user: User
):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    image.title = body.title
    image.description = body.description
    await db.commit()
    await db.refresh(image)
    return image


async def delete_image(image_id: int, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    await db.delete(image)
    await db.commit()
    return image


async def transform_image(
    image_id: int, tr_url: str, db: AsyncSession, current_user: User
):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    image.transform_url = tr_url
    await db.commit()
    await db.refresh(image)
    return image


async def get_base_url(image_id: int, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found image by id: {image_id}",
        )

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    return image.base_url


async def get_all_images(db: AsyncSession):
    stmt = select(Image)
    res = await db.execute(stmt)
    images = res.scalars().all()
    return images


async def get_transform_url(image_id: int, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found image by id: {image_id}",
        )

    if image.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    return image.transform_url


async def qr_code(image_id: int, qr_url: str, db: AsyncSession, current_user: User):
    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")

    image.qr_url = qr_url
    await db.commit()
    await db.refresh(image)
    return image
