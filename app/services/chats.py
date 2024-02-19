from app.schemas.chats import ChatAddSchema, ChatJoinSchema, ChatSchema
from app.schemas.users import UserRead
from app.utils.service import BaseService
from app.managers.passwords import password_manager
from app import exceptions


class ChatsService(BaseService):
    async def get_all_chats(self):
        async with self.uow as uow:
            chats = await uow.chats.find_all()
            return [ChatSchema.model_validate(chat) for chat in chats]

    async def get_user_created_chats(self, user: UserRead):
        async with self.uow as uow:
            chats = await uow.chats.find_all(creator_id=user.id)
            return [ChatSchema.model_validate(chat) for chat in chats]

    async def get_user_chats(self, user: UserRead):
        async with self.uow as uow:
            chats = await uow.chats.find_chats_user_is_member(user.id)
            return [ChatSchema.model_validate(chat) for chat in chats]

    async def get_user_chat_by_id(self, chat_id: int, user: UserRead):
        async with self.uow as uow:
            chat_in_db = await uow.chats.find_one_or_none(id=chat_id)

            if chat_in_db is None:
                raise exceptions.ChatIsNotExistsException()

            is_user_in_chat = await uow.chats.check_user_in_chat(chat_id, user.id)

            if is_user_in_chat is None:
                raise exceptions.ChatAccessDeniedException()

            return ChatSchema.model_validate(chat_in_db)

    async def get_chat_by_id(self, chat_id: int):
        async with self.uow as uow:
            chat = await uow.chats.find_one_or_none(id=chat_id)

            if chat is None:
                raise exceptions.ChatIsNotExistsException()

            return ChatSchema.model_validate(chat)

    async def delete_chat_by_id(self, chat_id: int, user: UserRead):
        async with self.uow as uow:
            chat = await uow.chats.find_one_or_none(id=chat_id)

            if chat is None:
                raise exceptions.ChatIsNotExistsException()

            if chat.creator_id != user.id:
                raise exceptions.ChatDeletionPermissionsException()

            await uow.chats.delete(id=chat.id)
            await uow.commit()

            return True

    async def add_chat(self, chat: ChatAddSchema, user: UserRead):
        chat_dict = chat.model_dump()
        chat_dict["creator_id"] = user.id

        if password := chat_dict.get("password"):
            chat_dict["is_private"] = True
            chat_dict["hashed_password"] = password_manager.get_password_hash(password)

        del chat_dict["password"]

        async with self.uow as uow:
            chat_id = await uow.chats.add_one(**chat_dict)
            chat_in_db = await uow.chats.find_chat_with_members(chat_id)
            user_in_db = await uow.users.find_one_or_none(id=user.id)
            chat_in_db.members.append(user_in_db)
            await uow.commit()

            return chat_id

    async def add_member_to_chat(self, chat: ChatJoinSchema, user: UserRead):
        async with self.uow as uow:
            chat_in_db = await uow.chats.find_chat_with_members(chat.id)

            if chat_in_db.is_private and not password_manager.verify_password(
                chat.password, chat_in_db.hashed_password
            ):
                raise exceptions.ChatPasswordMismatchException()

            user_in_db = await uow.users.find_one_or_none(id=user.id)
            chat_in_db.members.append(user_in_db)
            await uow.commit()

    async def remove_member_from_chat(self, chat_id: int, user: UserRead):
        async with self.uow as uow:
            chat_in_db = await uow.chats.find_chat_with_members(chat_id)
            user_in_db = await uow.users.find_one_or_none(id=user.id)
            chat_in_db.members.remove(user_in_db)
            await uow.commit()
