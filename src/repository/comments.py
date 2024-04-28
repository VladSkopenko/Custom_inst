from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import detail_message
from src.database.models import Comment
from src.database.models import User
from src.schemas.comments import CommentSchema


async def create_comment(
    image_id: int, body: CommentSchema, db: AsyncSession, current_user: User
) -> Optional[Comment]:
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

    stmt = select(Comment).filter_by(id=comment_id, user=current_user)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()

    if not comment:
        return None

    if comment.user_id != current_user.id and current_user.role not in (
        "admin",
        "moderator",
    ):
        return None

    comment.comment = body.comment
    db.add(comment)

    await db.commit()
    await db.refresh(comment)

    return comment


async def delete_comment(comment_id: int, db: AsyncSession, current_user: User):

    stmt = select(Comment).filter_by(id=comment_id, user_id=current_user.id)
    comment = await db.execute(stmt)
    comment = comment.scalar_one_or_none()
    if comment:
        if current_user.role == "admin":
            await db.delete(comment)
            await db.commit()
            return comment
        elif comment.user_id == current_user.id:
            await db.delete(comment)
            await db.commit()
            return comment
        else:
            raise HTTPException(status_code=403, detail=detail_message.PERMISSION_ERROR)
    else:
        raise HTTPException(status_code=404, detail=detail_message.FILE_NOT_FOUND)
