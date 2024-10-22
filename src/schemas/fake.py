from pydantic import BaseModel


class FakeUserResponse(BaseModel):
    id: int
    username: str
    avatarUrl: str
    description: str
    subscriptionsAmount: int
    firstName: str
    lastName: str
    isActive: bool
    stack: list[str]
    city: str


class FakePaginatedResponse(BaseModel):
    items: list[FakeUserResponse]
    total: int
    page: int
    size: int
    pages: int
