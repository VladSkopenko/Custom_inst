from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.database.models import Role

class UserSchema(BaseModel):
    nickname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int = 1
    nickname: str
    email: EmailStr
    role: Role
    is_active: bool
   
    model_config = ConfigDict(from_attributes = True)  # noqa


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    
class RequestEmail(BaseModel):
    email: EmailStr
    

class PasswordChangeRequest(BaseModel):
    password: str
    confirm_password: str