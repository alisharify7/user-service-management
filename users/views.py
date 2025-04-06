import uuid
from typing import List

from fastapi import Depends, HTTPException
from starlette import status as http_status

import sqlalchemy as sa
import sqlalchemy.orm as so
from starlette.responses import JSONResponse

from core.db import get_session
from core.extensions import hashManager

from users import users_router
from users.model import User as UserModel
from users.scheme import CreateUserScheme, DumpUserScheme, UpdateUserScheme


@users_router.post("/", response_model=DumpUserScheme)
async def create_user(
    user_data: CreateUserScheme, db_session: so.Session = Depends(get_session)
):
    """creating new user in database."""
    query = sa.select(UserModel).filter(
        sa.or_(
            UserModel.username == user_data.username,
            UserModel.phone_number == user_data.phone_number,
            UserModel.email_address == user_data.email_address,
        )
    )
    result = db_session.execute(query).scalar_one_or_none()
    if result:
        if result.username == user_data.username:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="Username already exists.",
            )
        elif result.phone_number == user_data.phone_number:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="Phone number already exists.",
            )
        elif result.email_address == user_data.email_address:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="Email address already exists.",
            )

    new_user = UserModel(**user_data.model_dump())
    new_user.set_password(new_user.password)
    new_user.set_public_key()
    db_session.add(new_user)

    try:
        db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"there was an error in the saving the user in db. check logs for more info. + {e.args}",
        )
    db_session.refresh(new_user)
    return new_user


@users_router.get("/id/{user_id}", response_model=DumpUserScheme)
async def get_user_by_id(user_id: int, db_session: so.Session = Depends(get_session)):
    """retrieve a user with  id """
    query = sa.select(UserModel).filter_by(id=user_id)
    result = db_session.execute(query).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="there is no user with given id.")
    return result

@users_router.get("/username/{username}", response_model=DumpUserScheme)
async def get_user_by_username(username: str, db_session: so.Session = Depends(get_session)):
    """retrieve a user with a username """
    query = sa.select(UserModel).filter_by(username=username)
    result = db_session.execute(query).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="there is no user with given username.")
    return result


@users_router.get("/public_key/{public_key}", response_model=DumpUserScheme)
async def get_user_by_public_key(public_key: str, db_session: so.Session = Depends(get_session)):
    """retrieve a user with a public-key """
    query = sa.select(UserModel).filter_by(public_key=public_key)
    result = db_session.execute(query).scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="there is no user with given public_key.")
    return result

@users_router.get("/", response_model=List[DumpUserScheme])
async def get_all_users(db_session: so.Session = Depends(get_session)):
    """returns all users in pagination"""
    # TODO: add pagination
    query = sa.select(UserModel)
    result = db_session.execute(query).scalars().all()
    if not result:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="there is no user in db.")
    return result

@users_router.put("/{user_id}", status_code=http_status.HTTP_204_NO_CONTENT)
async def update_user(user_id: int, user_data: UpdateUserScheme, db_session: so.Session = Depends(get_session)):
    """Update a specific user"""
    user_data = user_data.model_dump()
    user_data["password"] = hashManager.hash(user_data["password"])
    query = sa.update(UserModel).where(UserModel.id==user_id).values(
        **user_data
    )
    try:
        result = db_session.execute(query)
        db_session.commit()
        if result.rowcount > 0:
            return {}
        else:
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="User not found or no changes made")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="An error occurred")
@users_router.delete("/id/{user_id}", status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db_session: so.Session = Depends(get_session)):
    """delete a user with given user id"""
    query = sa.delete(UserModel).filter_by(id=user_id)
    try:
        result = db_session.execute(query)
        db_session.commit()
        if result.rowcount > 0:
            return {}
        else:
            raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="User not found or no changes made")
    except Exception as e:
        print(e)
        db_session.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred"
        )

    return {}
