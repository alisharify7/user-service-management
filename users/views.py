from users import users_router
from users.model import User

@users_router.post("/")
async def create_user():
    return {"msg": "OK"}


@users_router.put("/")
async def update_user():
    return {"msg": "OK"}


@users_router.delete("/{user_id}")
async def delete_user(user_id:int):
    return {"msg": "OK"}


@users_router.get("/{user_id}")
async def get_user(user_id:int):
    return {"msg": "OK"}