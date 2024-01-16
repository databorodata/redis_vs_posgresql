from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False



class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str]
    email: str = Optional[str]
    password: str = Optional[str]
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None