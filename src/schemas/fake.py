from pydantic import BaseModel

class FakeUserResponse(BaseModel):
    id: int
    username: str
    avatarUrl: str
    subscriptionsAmount: int
    firstName: str
    lastName: str
    isActive: bool
    stack: list[str]
    city: str

