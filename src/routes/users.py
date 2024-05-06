from fastapi import APIRouter
from fastapi import Depends

from src.database.models import User
from src.schemas.users import UserResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
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
    :doc-author: Trelent
    """
    return user
