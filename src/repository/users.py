from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.users import UserSchema


async def get_admin_exist(db: AsyncSession = Depends(get_db)):
    """
    Check if admin exists.

    :param db: AsyncSession
    :return: True if admin exists, False otherwise
    """

    stmt = select(User).where(User.role == Role.admin)
    user = await db.execute(stmt)
    result = user.scalar_one_or_none()
    return result is not None


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Get user by email.

    :param email: str
    :param db: AsyncSession
    :return: User
    """

    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    Create new user.

    :param body: UserSchema
    :param db: AsyncSession
    :return: User
    """

    new_user = User(**body.model_dump())

    if await get_admin_exist(db):
        new_user.role = Role.user
    else:
        new_user.role = Role.admin
        new_user.confirmed = True

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as err:
        print(f"ERROR create_user {err}")


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update user token.

    :param user: User
    :param token: str
    :param db: AsyncSession
    :return: None
    """

    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Confirmed email.

    :param email: str
    :param db: AsyncSession
    :return: None
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()
