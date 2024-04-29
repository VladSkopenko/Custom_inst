from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import User
from src.repository.comments import create_comment
from src.repository.comments import delete_comment
from src.repository.comments import edit_comment
from src.schemas.comments import CommentResponseSchema
from src.schemas.comments import CommentSchema
from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post(
    "/create", response_model=CommentResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_comment_route(
    image_id: int,
    body: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_comment_route function creates a comment for an image.
        The function takes in the following parameters:
            - image_id: int, the id of the image to create a comment for.
            - body: CommentSchema, which is used to validate and deserialize data sent by users.
                It contains two fields (text and user_id) that are required when creating comments.

    :param image_id: int: Get the image id from the url
    :param body: CommentSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :param : Get the image id from the url
    :return: A comment object
    :doc-author: Trelent
    """
    comment = await create_comment(image_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return comment


@router.put("/edit/{comment_id}/", response_model=CommentResponseSchema)
async def edit_comment_route(
    comment_id: int,
    body: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The edit_comment_route function allows a user to edit an existing comment.
        The function takes in the following parameters:
            - comment_id: int, the id of the comment that is being edited.
            - body: CommentSchema, a schema containing all of the information needed to update a given file's metadata.
                This includes fields such as title and description (see models/comment_schema for more details).

    :param comment_id: int: Get the comment id from the url
    :param body: CommentSchema: Validate the data in the body of a request
    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the current user
    :param : Get the comment_id from the url
    :return: A comment object
    :doc-author: Trelent
    """
    comment = await edit_comment(comment_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return comment


@router.delete("/delete/{comment_id}/", response_model=CommentResponseSchema)
async def delete_comment_route(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_comment_route function deletes a comment from the database.

    :param comment_id: int: Get the comment_id from the url
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user from the auth_service
    :param : Get the id of the comment to be deleted
    :return: The deleted comment
    :doc-author: Trelent
    """
    comment = await delete_comment(comment_id, db, current_user)
    return comment
