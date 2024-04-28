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
from src.schemas.comments import CommentSchema,CommentResponseSchema
from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/create", response_model=CommentResponseSchema,
             status_code=status.HTTP_201_CREATED)
async def create_comment_route(
        image_id: int,
        body: CommentSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
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
    comment = await delete_comment(comment_id, db, current_user)
    return comment
