from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatAddSchema(BaseModel):
    name: str
    password: Optional[str] = None


class ChatSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    creator_id: int
    is_private: bool


class ChatJoinSchema(BaseModel):
    id: int
    password: str
