from fastapi import Depends

import sqlalchemy.orm as so

from core.db import get_session
from users import users_router
from users.model import User
from users.scheme import CreateUserScheme

@users_router.post("/")
async def create_user(user_data: CreateUserScheme, db_session: so.Session = Depends(get_session)):
    db_session.add
    return {"msg": "OK"}


@users_router.put("/{user_id}")
async def update_user(user_id: int,  db_session: so.Session  = Depends(get_session)):
    return {"msg": "OK"}


@users_router.delete("/{user_id}")
async def delete_user(user_id:int,  db_session: so.Session  = Depends(get_session)):
    return {"msg": "OK"}


@users_router.get("/{user_id}")
async def get_user(user_id: int, db_session: so.Session  = Depends(get_session)):
    return {"msg": "OK"}