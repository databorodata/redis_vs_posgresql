from pydantic import BaseModel, EmailStr
from typing import Optional, Generic, TypeVar

ID = TypeVar("ID")  # Это может быть, например, str или UUID

class User(BaseModel, Generic[ID]):
    id: Optional[ID] = None  # ID пользователя (может быть str, UUID и т.д.)
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True  # По умолчанию пользователь активен
    is_superuser: bool = False  # По умолчанию пользователь не является суперпользователем
    is_verified: bool = False  # По умолчанию email пользователя не подтвержден
