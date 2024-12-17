from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.user.events.user_created import UserCreated
from src.domain.user.exceptions import (
    UserIsDeletedError,
)
from src.domain.user.value_objects import FullName, TgUserId, UserId
from src.domain.user.value_objects.deleted_status import DeletionTime


@dataclass
class User(AggregateRoot):
    id: UserId
    full_name: FullName
    telegram_id: TgUserId
    deleted_at: DeletionTime = field(default=DeletionTime.create_not_deleted(), kw_only=True)

    @classmethod
    def create(
        cls,
        user_id: UserId,
        full_name: FullName,
        telegram_id: TgUserId
    ) -> Self:
        user = cls(user_id, full_name, telegram_id)
        user.record_event(
            UserCreated(
                user_id.to_raw(),
                full_name.first_name,
                full_name.last_name,
                telegram_id.to_raw(),
            ),
        )
        return user

    def _validate_not_deleted(self) -> None:
        if self.deleted_at.is_deleted():
            raise UserIsDeletedError(self.id.to_raw())
