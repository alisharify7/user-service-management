from fastapi import Depends, HTTPException
from starlette import status as http_status

import sqlalchemy as sa
import sqlalchemy.orm as so

from core.db import get_session

from users import users_router
from users.model import User as UserModel
from users.scheme import CreateUserScheme


@users_router.post("/")
async def create_user(
    user_data: CreateUserScheme, db_session: so.Session = Depends(get_session)
):
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
    return {"msg": "user created successfully", "user_info": new_user}


@users_router.get("/{user_id}")
async def get_user(user_id: int, db_session: so.Session = Depends(get_session)):
    return {"msg": "OK"}


@users_router.put("/{user_id}")
async def update_user(user_id: int, db_session: so.Session = Depends(get_session)):
    return {"msg": "OK"}


@users_router.delete("/{user_id}")
async def delete_user(user_id: int, db_session: so.Session = Depends(get_session)):
    return {"msg": "OK"}
