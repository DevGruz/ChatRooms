from fastapi import APIRouter

from app.api.api_v1.endpoints import chats, users
from app.managers.users import fastapi_users
from app.core.auth import auth_backend
from app.schemas.users import UserRead, UserCreate, UserUpdate

api_router = APIRouter()
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
