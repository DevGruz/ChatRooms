from app.schemas.messages import MessageAddSchema
from app.utils.service import BaseService
from app.schemas.messages import MessageWithUserDetailSchema


class MessagesService(BaseService):
    async def add_message(
        self, message: MessageAddSchema
    ) -> MessageWithUserDetailSchema:
        message_dict = message.model_dump()
        async with self.uow as uow:
            message_id = await uow.messages.add_one(**message_dict)
            await uow.commit()
            message = await uow.messages.find_message_with_user_detail(message_id)
            message_schema = MessageWithUserDetailSchema.model_validate(message)
            return message_schema

    async def get_message_by_id(self, message_id: int) -> MessageWithUserDetailSchema:
        async with self.uow as uow:
            message = await uow.messages.find_message_with_user_detail(message_id)
            message_schema = MessageWithUserDetailSchema.model_validate(message)
            return message_schema

    async def get_all_chat_messages(self, chat_id: int):
        async with self.uow as uow:
            messages = await uow.messages.find_all_chat_messages(chat_id)
            messages_schema = [
                MessageWithUserDetailSchema.model_validate(row) for row in messages
            ]
            return messages_schema

    async def get_recent_chat_messages(
        self, chat_id: int, count: int
    ) -> list[MessageWithUserDetailSchema]:
        async with self.uow as uow:
            messages = await uow.messages.find_recent_chat_messages(chat_id, count)
            messages_schema = [
                MessageWithUserDetailSchema.model_validate(row) for row in messages
            ]
            return messages_schema
