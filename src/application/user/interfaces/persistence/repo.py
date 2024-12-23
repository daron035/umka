from abc import abstractmethod
from typing import Protocol

from src.domain.grade.entities import GradeEntity
from src.domain.user.entities import UserEntity
from src.domain.user.value_objects import TgUserId


class UserRepo(Protocol):
    @abstractmethod
    async def add_user(self, user: UserEntity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
        raise NotImplementedError


class GradeBookRepo(Protocol):
    @abstractmethod
    async def add(self, grade: GradeEntity) -> None:
        raise NotImplementedError
