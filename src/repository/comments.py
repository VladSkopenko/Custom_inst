from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Comment
from src.database.models import Role
from src.database.models import User
from src.schemas.comments import CommentSchema


async def create_comment(
    image_id: int, body: CommentSchema, db: AsyncSession, current_user: User
) -> Optional[Comment]:
    """
    The create_comment function creates a new comment for an image.

    :param image_id: int: Specify the image that the comment is being created for
    :param body: CommentSchema: Validate the request body
    :param db: AsyncSession: Pass the database connection to the function
    :param current_user: User: Get the user_id of the current user
    :return: A comment object
    :doc-author: Trelent
    """
    comment_data: Comment = Comment(
        image_id=image_id, user_id=current_user.id, comment=body.comment
    )
    db.add(comment_data)
    await db.commit()
    await db.refresh(comment_data)
    return comment_data


async def edit_comment(
    comment_id: int, body: CommentSchema, db: AsyncSession, current_user: User
) -> Comment | None:
    """
    The edit_comment function allows a user to edit their own comment.
        The function takes in the comment_id, body, db and current_user as parameters.
        It then checks if the user is authorized to edit this particular comment by checking if they are either an admin or moderator or if they are the owner of that specific comment.
        If not it raises a 403 error with a message saying permission denied.
        If so it updates the database with new information from body and returns that updated information.

    :param comment_id: int: Get the comment from the database
    :param body: CommentSchema: Validate the request body
    :param db: AsyncSession: Access the database
    :param current_user: User: Get the current user's id
    :return: The edited comment
    :doc-author: Trelent
    """
    stmt = (
        select(Comment)
        .filter(Comment.id == comment_id)
        .filter(Comment.user.has(id=current_user.id))
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    if comment.user_id != current_user.id and current_user.role not in (
        Role.admin,
        Role.moderator,
    ):
        raise HTTPException(status_code=403, detail=detail_message.PERMISSION_ERROR)
    comment.comment = body.comment
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, db: AsyncSession, current_user: User):
    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            db (AsyncSession): An async session object for interacting with the database.
            current_user (User): The user who is making this request, as determined by FastAPI's security system.

    :param comment_id: int: Identify the comment to be deleted
    :param db: AsyncSession: Access the database
    :param current_user: User: Get the current user's id
    :return: The deleted comment
    :doc-author: Trelent
    """
    stmt = select(Comment).filter_by(id=comment_id, user_id=current_user.id)
    comment = await db.execute(stmt)
    comment = comment.scalar_one_or_none()
    if comment:
        if current_user.role in (Role.admin, Role.moderator):
            await db.delete(comment)
            await db.commit()
            return comment
        else:
            raise HTTPException(status_code=403, detail=detail_message.PERMISSION_ERROR)
    else:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)


async def get_comment(comment_id: int, db: AsyncSession):
    """
    The get_comment function returns a comment object from the database.
        Args:
            comment_id (int): The id of the comment to be retrieved.
            db (AsyncSession): An async session for querying the database.

    :param comment_id: int: Specify the id of the comment to be retrieved
    :param db: AsyncSession: Pass the database session to the function
    :return: A comment object
    :doc-author: Trelent
    """
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment:
        return comment
    else:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
