from fastapi import APIRouter

users_router = APIRouter()

import users.views
import users.model
