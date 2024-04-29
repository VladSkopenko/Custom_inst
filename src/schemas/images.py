from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageSchema(BaseModel):
    title: str | None = None
    description: str | None = None


class ImageResponseSchema(BaseModel):
    id: int
    user_id: int | None
    title: str | None
    base_url: str | None
    transform_url: str | None
    description: str | None
    qr_url: str | None
    created_at: datetime
    updated_at: datetime

    class Config(ConfigDict):
        from_attributes = True
