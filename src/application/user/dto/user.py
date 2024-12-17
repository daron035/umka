from dataclasses import dataclass, field
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class User(DTO):
    id: UUID
    username: str
    first_name: str
    last_name: str
    telegram_id: int | None
    deleted_at: None = field(default=None, init=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
