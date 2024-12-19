from typing import Protocol

from src.domain.user.value_objects.tg_user_id import TgUserId
from src.domain.user.value_objects.user_id import UserId


class UserReader(Protocol):
    async def get_user_by_tg_id(self, telegram_id: TgUserId) -> UserId:
        raise NotImplementedError
