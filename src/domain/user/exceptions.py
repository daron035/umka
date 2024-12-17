from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class UserIsDeletedError(RuntimeError, DomainError):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'


@dataclass(eq=False)
class TelegramUserAlreadyExistsError(DomainError):
    full_name: str
    telegram_id: int | None = None

    @property
    def title(self) -> str:
        if self.telegram_id is None:
            return f'The user "{self.full_name}" already exists'
        return f'The user "{self.full_name}" with the "{self.telegram_id}" telegram_id already exists'
