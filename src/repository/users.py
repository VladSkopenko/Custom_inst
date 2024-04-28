from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.users import UserSchema

async def get_admin_exist(db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(User.role == Role.admin)
    user = await db.execute(stmt)
    result = user.scalar_one_or_none()
    return result is not None

async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    
    new_user = User(**body.model_dump())
    # Перевіряємо, чи існує адміністратор
    if await get_admin_exist(db):
        new_user.role = Role.user  # Якщо адміністратор існує, новий користувач отримує роль 'user'
    else:
        new_user.role = Role.admin  # Якщо адміністратор ще не існує, новий користувач отримує роль 'admin'
    
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as err:
        print(f"ERROR create_user {err}")
    


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


