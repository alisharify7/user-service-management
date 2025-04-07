from fastapi_pagination import Page, Params
from fastapi import Depends, HTTPException, Query
from fastapi_pagination.ext.sqlalchemy import paginate

from starlette import status as http_status

import sqlalchemy as sa
import sqlalchemy.orm as so

from core.db import get_session

from users import users_router
from users.model import User as UserModel
from users.scheme import CreateUserScheme, DumpUserScheme, UpdateUserScheme

import users.operations as user_operations


@users_router.post("/", response_model=DumpUserScheme)
async def create_user(
    user_data: CreateUserScheme, db_session: so.Session = Depends(get_session)
):
    """creating new user in database."""
    result = user_operations.create_user(
        user_data=user_data, db_session=db_session
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])
    return result[0]


@users_router.get("/id/{user_id}", response_model=DumpUserScheme)
async def get_user_by_id(
    user_id: int, db_session: so.Session = Depends(get_session)
):
    """retrieve a user with  id"""
    result = user_operations.get_user_by_id(
        user_data=user_id, db_session=db_session
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])
    return result[0]


@users_router.get("/username/{username}", response_model=DumpUserScheme)
async def get_user_by_username(
    username: str, db_session: so.Session = Depends(get_session)
):
    """retrieve a user with a username"""
    result = user_operations.get_user_by_username(
        username=username, db_session=db_session
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])
    return result[0]


@users_router.get("/public_key/{public_key}", response_model=DumpUserScheme)
async def get_user_by_public_key(
    public_key: str, db_session: so.Session = Depends(get_session)
):
    """retrieve a user with a public-key"""
    result = user_operations.get_user_by_public_key(
        public_key=public_key, db_session=db_session
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])

    return result[0]


def get_all_users_pagination(
    page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)
) -> Params:
    return Params(page=page, size=size)


@users_router.get("/", response_model=Page[DumpUserScheme])
async def get_all_users(
    params: Params = Depends(get_all_users_pagination),
    db_session: so.Session = Depends(get_session),
):
    return paginate(db_session, sa.select(UserModel), params)


@users_router.put("/{user_id}", status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(
    user_id: int,
    user_data: UpdateUserScheme,
    db_session: so.Session = Depends(get_session),
):
    """Update a specific user"""
    result = user_operations.update_user(
        user_id=user_id, db_session=db_session, user_data=user_data
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])

    return result[0]


@users_router.delete(
    "/id/{user_id}", status_code=http_status.HTTP_204_NO_CONTENT
)
async def delete_user_by_id(
    user_id: int, db_session: so.Session = Depends(get_session)
):
    """delete a user with given user id"""
    result = user_operations.delete_user(
        user_id=user_id, db_session=db_session
    )
    if len(result) != 1:
        raise HTTPException(status_code=result[0], detail=result[1])

    return result[0]
