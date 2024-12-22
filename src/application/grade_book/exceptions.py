from dataclasses import dataclass

from src.application.common.exceptions import ApplicationError


@dataclass(eq=False)
class SubjectExistError(ApplicationError):
    name: str

    @property
    def title(self) -> str:
        return f'A subject with "{self.name}" name doesn\'t exist'
