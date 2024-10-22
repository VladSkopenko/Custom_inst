from typing import List

from fastapi import APIRouter
from fastapi import Depends

from src.database.models import User
from src.repository.fake import create_fake_followers
from src.repository.fake import create_fake_user
from src.repository.fake import get_fake_user
from src.schemas.fake import FakePaginatedResponse
from src.schemas.fake import FakeUserResponse
from src.schemas.users import UserResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=FakeUserResponse)
async def get_current_user(
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_current_user function is a dependency that will be injected into the function below.
    It will return the current user if they are authenticated, or None otherwise.

    :param user: User: Get the current user
    :param dependencies: Add a rate limiter to the function
    :param seconds: Set the time interval for which the rate limiter is active
    :return: The user object
    """
    fake_user = get_fake_user()
    return fake_user


@router.get("/some_user_card", response_model=List[FakeUserResponse])
async def get_some_user_card():
    """SImple router for test front-end"""
    some_users = await create_fake_user()
    return some_users


@router.get("/fake_followers", response_model=FakePaginatedResponse)
async def get_fake_followers():
    """SImple router for test front-end"""
    fake_followers = await create_fake_followers()
    return fake_followers