"""
* users management
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/user-service-management
"""

from typing import Optional, Union

from pydantic import BaseModel, EmailStr, constr, ConfigDict
from enum import Enum
from users.model import Gender


class CreateUserScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: constr(max_length=256)
    password: constr(max_length=128)
    email_address: Optional[EmailStr] = None
    phone_number: Optional[constr(max_length=16)] = None
    gender: Optional[Gender] = None


class BaseDumpUserScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: constr(max_length=256)
    email_address: EmailStr
    phone_number: constr(max_length=16)
    gender: Gender


class DumpUserScheme(BaseDumpUserScheme):
    public_key: str
    id: int


class UpdateUserScheme(BaseDumpUserScheme):
    password: constr(max_length=128)


class UserEventType(str, Enum):
    CREATED = "user.created"
    UPDATED = "user.updated"
    DELETED = "user.deleted"


class CreateUserEvent(CreateUserScheme):
    pass


class UpdateUserEvent(UpdateUserScheme):
    pass


class DeleteUserEvent(BaseModel):
    id: int


class UserEvent(BaseModel):
    event_type: UserEventType
    data: Union[CreateUserEvent, UpdateUserEvent, DeleteUserEvent]
