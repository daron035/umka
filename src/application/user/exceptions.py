from dataclasses import dataclass
from uuid import UUID

from src.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class UserIdAlreadyExistsError(ApplicationError):
    user_id: UUID | int

    @property
    def title(self) -> str:
        return f'A user with the "{self.user_id}" user_id already exists'


@dataclass(eq=False)
class UserIdNotExistError(ApplicationError):
    user_id: UUID | int

    @property
    def title(self) -> str:
        return f'A user with "{self.user_id}" user_id doesn\'t exist'
