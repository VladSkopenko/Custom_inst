from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.db import get_db
from src.database.models import Role
from src.database.models import User
from src.repository.comments import create_comment
from src.repository.comments import delete_comment
from src.repository.comments import edit_comment
from src.repository.comments import get_comment
from src.schemas.comments import CommentResponseSchema
from src.schemas.comments import CommentSchema
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/comments", tags=["comments"])

access_to_route_delete = RoleAccess([Role.admin, Role.moderator])


@router.post(
    "/create/{comment_id}",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment_route(
    image_id: int,
    body: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_comment_route function creates a comment for an image.

    :param image_id: int: Get the image id from the url
    :param body: CommentSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :param : Get the image id from the url

    :return: A comment object
    """

    comment = await create_comment(image_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return comment


@router.put("/edit/{comment_id}", response_model=CommentResponseSchema)
async def edit_comment_route(
    comment_id: int,
    body: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The edit_comment_route function allows a user to edit an existing comment.

    :param comment_id: int: Get the comment id from the url
    :param body: CommentSchema: Validate the data in the body of a request
    :param db: AsyncSession: Get the database session
    :param current_user: User: Get the current user
    :param : Get the comment_id from the url

    :return: A comment object
    """

    comment = await edit_comment(comment_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return comment


@router.delete(
    "/delete/{comment_id}",
    response_model=CommentResponseSchema,
    dependencies=[Depends(access_to_route_delete)],
)
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
    """

    comment = await delete_comment(comment_id, db, current_user)
    return comment


@router.get("/{comment_id}", response_model=CommentResponseSchema)
async def get_comment_route(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    The get_comment_route function is a route that returns the comment with the given id.

    :param comment_id: int: Get the comment id from the url path
    :param db: AsyncSession: Get a database session, which is used when executing sqlalchemy commands
    :param : Get the comment id from the url

    :return: The comment object
    """

    comment = await get_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
    return comment
