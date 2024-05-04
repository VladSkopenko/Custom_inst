from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Tag
from src.database.models import User
from src.schemas.tags import TagSchema


async def get_tag(tag_name: str, db: AsyncSession, current_user: User):
    """
    The get_tag function is used to retrieve a tag from the database.
        It takes in a tag_name and returns the corresponding Tag object.
        If no such tag exists, it raises an HTTPException with status code 404.

    :param tag_name: str: Specify the name of the tag that is being searched for
    :param db: AsyncSession: Access the database
    :param current_user: User: Get the user id of the current user
    :return: A tag object
    :doc-author: Trelent
    """
    stmt = select(Tag).where(Tag.tag_name == tag_name)
    existing_tag = await db.execute(stmt)
    tag = existing_tag.scalar_one_or_none()
    if tag:
        return tag


async def create_tag(body: TagSchema, db: AsyncSession, current_user: User):
    """
    The create_tag function creates a new tag in the database.
        It takes in a TagSchema object, which is validated by pydantic.
        The function then checks to see if the tag already exists, and returns it if so.
        If not, it creates a new Tag object and adds it to the database.

    :param body: TagSchema: Get the tag_name and tag_type from the request body
    :param db: AsyncSession: Create a database connection
    :param current_user: User: Make sure that the user is logged in
    :return: A tag object
    :doc-author: Trelent
    """
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
    """
    The delete_tag function deletes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be deleted.
            db (AsyncSession): An async session object for interacting with the database.
                This is provided by FastAPI's dependency injection system, and should not be created manually.

    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: AsyncSession: Access the database
    :param current_user: User: Check if the user is logged in
    :return: The deleted tag
    :doc-author: Trelent
    """
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
