from pydantic import BaseModel

from pydantic import Field

from datetime import datetime


class CommentSchema(BaseModel):
    comment: str = Field(min_length=3, max_length=500)


class CommentResponseSchema(BaseModel):
    id: int
    user_id: int
    image_id: int
    comment: str
    created_at: datetime
    updated_at: datetime
