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

    """
The add_tag_to_image function adds a tag to an image.
    Args:
        image_id (int): The id of the image to which we want to add a tag.
        body (TagSchema): A TagSchema object containing the name of the new tag.

:param image_id: int: Get the image id
:param body: TagSchema: Get the tag name from the request body
:param db: AsyncSession: Pass a database connection to the function
:param current_user: User: Check if the user is logged in
:return: A string
:doc-author: Trelent
"""
    image = await get_image(image_id, db, mode="add_tag_to_image")
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

    """
The remove_tag_from_image function removes a tag from an image.
    Args:
        image_id (int): The id of the image to remove the tag from.
        tag_name (str): The name of the tag to be removed.

:param image_id: int: Find the image in the database
:param tag_name: str: Get the tag name from the request body
:param db: AsyncSession: Connect to the database
:param current_user: User: Check if the user is logged in
:return: A string
:doc-author: Trelent
"""
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

    """
The get_tags_by_image function returns a list of tag_ids associated with the image_id passed in as an argument.

:param image_id: int: Specify the image to get tags for
:param db: AsyncSession: Pass in the database connection
:return: A list of tag ids
:doc-author: Trelent
"""
    stmt = select(image_m2m_tag.c.tag_id).where(image_m2m_tag.c.image_id == image_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_data_image(image_id: int, db: AsyncSession):

    """
The get_data_image function takes in an image_id and a database connection.
It then returns a dictionary containing the following information:
    - The image itself, as returned by get_image()
    - A list of tags associated with the image, as returned by get_tags_by_image()
    - A list of comments associated with the image, as returned by get_comments()

:param image_id: int: Get the image from the database
:param db: AsyncSession: Pass the database connection to the function
:return: A dictionary with the following keys:
:doc-author: Trelent
"""
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
