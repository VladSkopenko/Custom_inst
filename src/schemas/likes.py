from pydantic import BaseModel

from pydantic import Field


class LikeSchema(BaseModel):
    grade: int = Field(ge=1, le=5)


class LikeResponseSchema(BaseModel):
    user_id: int
    image_id: int
    grade: int


class ImageRating(BaseModel):
    rating: float
