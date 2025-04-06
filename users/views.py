from users import users_router


@users_router.get("/hello/")
async def index():
    return {"msg": "OK"}