from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Image
from src.database.models import Role
from src.database.models import User
from src.schemas.images import ImageSchema


async def create_image(
    body: ImageSchema, base_url: str, db: AsyncSession, current_user: User
):
    """
    The create_image function creates an image in the database.

    :param body: ImageSchema: Get the data from the request body
    :param base_url: str: Pass the base url of the image
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: A created image object
    """

    image = Image(**body.dict())
    if image.title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail_message.TITLE_IS_REQUIRED,
        )
    image.base_url = base_url
    image.transform_url = base_url
    image.user_id = current_user.id
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image(image_id: int, db: AsyncSession, mode=1):
    """
    The get_image function takes in an image_id and a database session, and returns an image object if it exists.

    :param image_id: int: Specify the image you want to retrieve
    :param db: AsyncSession: Pass the database session
    :return: An image with the owner of a dictionary
    """

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
            "user": {
                "id": image.user_id,
                "nickname": image.user.nickname,
                "created_at": image.user.created_at,
                "role": image.user.role,
            },
        }
        return image_dict
    else:
        return image


async def update_image(
    image_id: int, body: ImageSchema, db: AsyncSession, current_user: User
):
    """
    The update_image function updates an image in the database.

    :param image_id: int: Specify the image you want to update
    :param body: ImageSchema: Pass the new image data
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: The updated image
    """

    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )

    image.title = body.title
    image.description = body.description
    await db.commit()
    await db.refresh(image)
    return image


async def delete_image(image_id: int, db: AsyncSession, current_user: User):
    """
    The delete_image function deletes an image from the database.

    :param image_id: int: Specify the image you want to delete
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: The deleted image
    """

    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )

    await db.delete(image)
    await db.commit()
    return image


async def transform_image(
    image_id: int, tr_url: str, db: AsyncSession, current_user: User
):
    """
    The transform_image function transforms an image.

    :param image_id: int: Specify the image you want to transform
    :param tr_url: str: Specify the transformed url
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: The transformed image
    """

    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )

    image.transform_url = tr_url
    await db.commit()
    await db.refresh(image)
    return image


async def get_base_url(image_id: int, db: AsyncSession, current_user: User):
    """
    Get base url of image

    :param image_id: int: Specify the image you want to get the base url
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: The base url of the image
    """

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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )
    return image.base_url


async def get_all_images(db: AsyncSession):
    """
    The get_all_images function returns all images from the database.

    :param db: AsyncSession: Pass the database session
    :return: A list of all images in the database
    """

    stmt = select(Image)
    res = await db.execute(stmt)
    images = res.scalars().all()
    return images


async def get_transform_url(image_id: int, db: AsyncSession, current_user: User):
    """
    The get_transform_url function returns the transform url of an image.

    :param image_id: int: Specify the image you want to get the transform url for
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: The transform url of the image
    """

    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found image by id: {image_id}",
        )

    if image.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )
    return image.transform_url


async def qr_code(image_id: int, qr_url: str, db: AsyncSession, current_user: User):
    """
    The qr_code function generates a QR code for an image.

    :param image_id: int: Specify the image you want to generate the QR code for
    :param qr_url: str: Specify the url of the QR code
    :param db: AsyncSession: Pass the database session
    :param current_user: User: Get the current user
    :return: An image with the qr_url of the image
    """

    stmt = select(Image).filter_by(id=image_id)
    res = await db.execute(stmt)
    image = res.scalar_one_or_none()

    if image is None:
        return None

    if image.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail_message.FORBIDDEN
        )

    image.qr_url = qr_url
    await db.commit()
    await db.refresh(image)
    return image


async def search_images(keyword: str, db: AsyncSession):
    """
    The search_images function searches for images in the database.

    :param keyword: str: Search for images with a specific keyword
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of image objects
    """
    stmt = None
    if keyword:
        stmt = select(Image).filter(
            or_(
                Image.description.ilike(f"%{keyword}%"),
                Image.title.ilike(f"%{keyword}%"),
            )
        )

    res = await db.execute(stmt)
    images = res.scalars().all()
    return images
