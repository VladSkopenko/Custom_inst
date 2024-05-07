from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class CommentSchema(BaseModel):
    comment: str = Field(min_length=3, max_length=500)


class CommentResponseSchema(BaseModel):
    id: int = 1
    user_id: int = 1
    image_id: int = 1
    comment: str
    created_at: datetime
    updated_at: datetime


