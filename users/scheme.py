from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
from users.model import Gender


class CreateUserScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: constr(max_length=256)
    password: constr(max_length=128)
    email_address: Optional[EmailStr] = None
    phone_number: Optional[constr(max_length=16)] = None
    gender: Optional[Gender] = None

    class Config:
        from_attributes = True  # Enables conversion from ORM objects (Pydantic v2)


class BaseDumpUserScheme(BaseModel):
    first_name: str
    last_name: str
    username: constr(max_length=256)
    email_address: EmailStr
    phone_number: constr(max_length=16)
    gender: Gender

    class Config:
        from_attributes = True  # Enables conversion from ORM objects (Pydantic v2)

class DumpUserScheme(BaseDumpUserScheme):
    public_key: str
    id: int

class UpdateUserScheme(BaseDumpUserScheme):
    password: constr(max_length=128)

