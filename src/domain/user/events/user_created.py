from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events.event import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    first_name: str
    last_name: str
    telegram_id: int | None
