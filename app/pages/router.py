from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.models.users import User
from app.managers.users import current_active_user
from app.api.deps import UOWDep
from app.services.chats import ChatsService

router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/chats/{chat_id}")
async def get_chat_page(
    request: Request,
    chat_id: int,
    uow: UOWDep,
    user: User = Depends(current_active_user),
):
    chat = await ChatsService(uow).get_user_chat_by_id(chat_id, user)
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "chat_name": chat.name,
            "chat_id": chat.id,
            "user_id": user.id,
        },
    )
