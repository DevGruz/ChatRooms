from sqlalchemy import (
    Table,
    Column,
    Integer,
    ForeignKey,
    CheckConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

user_chat = Table(
    "user_chat",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("chat_id", Integer, ForeignKey("chats.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("user_id", "chat_id", name="user_chat_pk"),
)


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_private: Mapped[bool] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)

    creator: Mapped["User"] = relationship(back_populates="created_chats")
    members: Mapped[list["User"]] = relationship(
        secondary="user_chat", back_populates="chats", cascade="all, delete"
    )
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")

    __table_args__ = (
        CheckConstraint(
            "(is_private = TRUE AND hashed_password IS NOT NULL AND hashed_password != '') OR (is_private = FALSE AND hashed_password IS NULL)",
            name="password_check",
        ),
    )

    def __str__(self):
        return f"Чат {self.id}"
