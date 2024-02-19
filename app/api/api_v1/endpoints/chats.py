from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.managers.connections import connection_manager
from app.services.messages import MessagesService
from app.services.chats import ChatsService
from app.schemas.chats import ChatSchema, ChatAddSchema, ChatJoinSchema
from app.schemas.messages import MessageAddSchema
from app.api.deps import websocket_auth, UOWDep, get_recent_chat_messages
from app.schemas.users import UserRead
from app.managers.users import current_active_user

router = APIRouter()


@router.get("/created_by")
async def get_user_created_chats(
    uow: UOWDep,
    user: UserRead = Depends(current_active_user),
) -> list[ChatSchema]:
    chats = await ChatsService(uow).get_user_created_chats(user)
    return chats


@router.get("/member_of")
async def get_chats_user_member(
    uow: UOWDep,
    user: UserRead = Depends(current_active_user),
) -> list[ChatSchema]:
    chats = await ChatsService(uow).get_user_chats(user)
    return chats


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: int,
    uow: UOWDep,
    user: UserRead = Depends(current_active_user),
):
    chat = await ChatsService(uow).delete_chat_by_id(chat_id, user)
    return chat


@router.post("/")
async def create_chat(
    uow: UOWDep,
    chat_schema: ChatAddSchema,
    user: UserRead = Depends(current_active_user),
):
    chat = await ChatsService(uow).add_chat(chat_schema, user)
    return chat


@router.post("/{chat_id}/join")
async def join_chat(
    uow: UOWDep,
    chat_id: int,
    chat: ChatJoinSchema,
    user: UserRead = Depends(current_active_user),
):
    await ChatsService(uow).add_member_to_chat(chat, user)
    return "success"


@router.post("/{chat_id}/leave")
async def leave_chat(
    uow: UOWDep,
    chat_id: int,
    user: UserRead = Depends(current_active_user),
):
    await ChatsService(uow).remove_member_from_chat(chat_id, user)
    return "success"


@router.get("/")
async def get_all_chats(
    uow: UOWDep,
) -> list[ChatSchema]:
    chats = await ChatsService(uow).get_all_chats()
    return chats


@router.websocket("/{chat_id}/ws")
async def websocket_chat(
    websocket: WebSocket,
    chat_id: int,
    uow: UOWDep,
    user=Depends(websocket_auth),
    recent_chat_messages=Depends(get_recent_chat_messages),
):
    await connection_manager.connect(websocket)

    try:
        for message in recent_chat_messages:
            message_json = message.model_dump_json()
            await connection_manager.send_personal_message(message_json, websocket)

        while True:
            data = await websocket.receive_text()
            message_schema = MessageAddSchema(
                text=data,
                chat_id=chat_id,
                sender_id=user.id,
            )
            message = await MessagesService(uow).add_message(message_schema)
            message_json = message.model_dump_json()
            await connection_manager.broadcast(message_json)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
