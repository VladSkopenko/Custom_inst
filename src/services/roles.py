from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from src.common import detail_message
from src.database.models import Role
from src.database.models import User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail_message.FORBIDDEN
            )
