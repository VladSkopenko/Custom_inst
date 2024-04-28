from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.comments import CommentSchema
from src.repository.comments import create_comment, edit_comment, delete_comment
from src.database.db import get_db

from fastapi import status
from src.database.models import User

from src.services.auth import auth_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/create", response_model=CommentSchema,
             status_code=status.HTTP_201_CREATED)
async def create_comment_route(
        image_id: int,
        body: CommentSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    comment = await create_comment(image_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail="Image not found")
    return comment


@router.put("/edit/{comment_id}/", response_model=CommentSchema)
async def edit_comment_route(
        comment_id: int,
        body: CommentSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    comment = await edit_comment(comment_id, body, db, current_user)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/delete/{comment_id}/", response_model=CommentSchema)
async def delete_comment_route(
        comment_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user),
):
    comment = await delete_comment(comment_id, db, current_user)
    return comment
