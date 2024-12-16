from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class UserIsDeletedError(RuntimeError, DomainError):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'
