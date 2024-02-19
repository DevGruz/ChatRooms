from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy import text as sa_text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas.messages import MessageSchema


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    timestamp: Mapped[datetime] = mapped_column(
        server_default=sa_text("TIMEZONE('utc', now())")
    )

    sender: Mapped["User"] = relationship(back_populates="messages")
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    def to_read_model(self) -> MessageSchema:
        return MessageSchema(
            id=self.id,
            text=self.text,
            sender_id=self.sender_id,
            chat_id=self.chat_id,
            timestamp=self.timestamp,
        )
