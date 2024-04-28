from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class CommentSchema(BaseModel):
    comment: str = Field(min_length=3, max_length=500)


