from abc import abstractmethod
from typing import Protocol

from src.domain.user import entities
from src.domain.user.value_objects import TgUserId


class UserRepo(Protocol):
    @abstractmethod
    async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: entities.User) -> None:
        raise NotImplementedError
