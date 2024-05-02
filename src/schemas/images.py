from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.users import UserResponse


class ImageSchema(BaseModel):
    title: str | None = None
    description: str | None = None


class ImageResponseSchema(BaseModel):
    id: int = 1
    user_id: int | None = 1
    title: str | None
    base_url: str | None
    transform_url: str | None
    description: str | None
    qr_url: str | None
    created_at: datetime
    updated_at: datetime
    user: UserResponse | None

    class Config(ConfigDict):
        from_attributes = True
