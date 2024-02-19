from typing import Annotated

from fastapi import WebSocket, Depends

from app.managers.users import fastapi_users, get_user_manager
from app.services.messages import MessagesService
from app.core.auth import auth_backend
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]

current_active_user = fastapi_users.current_user(active=True)


async def websocket_auth(
    websocket: WebSocket,
    user_manager=Depends(get_user_manager),
    strategy=Depends(auth_backend.get_strategy),
):
    try:
        cookie = websocket.cookies.get("access_token")
        user = await strategy.read_token(cookie, user_manager)

        if user and user.is_active:
            return user

        return None
    except Exception as e:
        print("exp in func websocket_auth: ", e)


async def get_recent_chat_messages(uow: UOWDep, chat_id: int):
    all_messages = await MessagesService(uow).get_all_chat_messages(chat_id)
    return all_messages
