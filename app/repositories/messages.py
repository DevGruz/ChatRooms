from app.utils.repository import SQLAlchemyRepository
from app.models.messages import Message
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class MessagesRepository(SQLAlchemyRepository):
    model = Message

    async def find_all_chat_messages(self, chat_id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.sender, innerjoin=True))
            .filter_by(chat_id=chat_id)
            .order_by(self.model.timestamp)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_recent_chat_messages(self, chat_id: int, count: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.sender, innerjoin=True))
            .filter_by(chat_id=chat_id)
            .order_by(self.model.timestamp)
            .limit(count)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_message_with_user_detail(self, message_id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.sender, innerjoin=True))
            .filter_by(id=message_id)
        )
        result = await self.session.execute(query)
        return result.scalars().one()
