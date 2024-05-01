from pydantic import BaseModel
from src.database.models import TagType
from typing import Optional
from enum import Enum


class TagTypeChoices(str, Enum):
    sport = "sport"
    animals = "animals"
    nature = "nature"
    people = "people"
    architecture = "architecture"


class TagSchema(BaseModel):
    tag_name: str
    tag_type: Optional[TagTypeChoices]

    class Config:
        use_enum_values = True


class TagResponseSchema(TagSchema):
    id: int

