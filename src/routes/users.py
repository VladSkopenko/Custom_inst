from typing import List

from fastapi import APIRouter
from fastapi import Depends
from faker import Faker

from src.database.models import User
from src.repository.fake import create_fake_user
from src.repository.fake import get_fake_user
from src.schemas.fake import FakeUserResponse
from src.schemas.users import UserResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])
fake = Faker("en")


@router.get("/me", response_model=FakeUserResponse)
async def get_current_user(
    user: User = Depends(auth_service.get_current_user),
):
    fake_user_for_front = get_fake_user()
    return fake_user_for_front


@router.get("/some_user_card", response_model=List[FakeUserResponse])
async def get_some_user_card():
    """SImple router for test front-end"""
    some_users = await create_fake_user()
    return some_users
