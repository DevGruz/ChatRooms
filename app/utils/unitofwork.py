from abc import ABC, abstractmethod
from typing import Type

from app.repositories.messages import MessagesRepository
from app.repositories.chats import ChatsRepository
from app.repositories.users import UsersRepository
from app.database import async_session_maker


class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    messages: Type[MessagesRepository]
    chats: Type[ChatsRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self._session = self.session_factory()
        self.users = UsersRepository(self._session)
        self.messages = MessagesRepository(self._session)
        self.chats = ChatsRepository(self._session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
