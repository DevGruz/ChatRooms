from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.users import UserRead


class MessageAddSchema(BaseModel):
    text: str
    chat_id: int
    sender_id: int


class MessageSchema(MessageAddSchema):
    id: int
    timestamp: datetime


class MessageWithUserDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    chat_id: int
    sender: "UserRead"
    timestamp: datetime
