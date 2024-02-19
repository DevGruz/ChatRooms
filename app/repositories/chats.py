from app.utils.repository import SQLAlchemyRepository
from app.models.chats import Chat
from app.models.users import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class ChatsRepository(SQLAlchemyRepository):
    model = Chat

    # async def add_one(self, **data):
    #     query = (
    #         insert(self.model)
    #         .values(**data)
    #         .returning(self.model)
    #     )
    #     result = await self.session.execute(query)
    #     return result.scalars().one()

    async def find_chat_with_members(self, chat_id: int):
        query = (
            select(self.model)
            .options(selectinload(self.model.members))
            .filter_by(id=chat_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one()

    async def find_chats_user_is_member(self, user_id: int):
        query = (
            select(self.model)
            .join(self.model.members)
            .options(selectinload(self.model.members))
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def check_user_in_chat(self, chat_id: int, user_id: int):
        query = (
            select(self.model)
            .join(self.model.members)
            .options(selectinload(self.model.members))
            .filter(self.model.id == chat_id, User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
