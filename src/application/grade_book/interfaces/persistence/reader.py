from typing import Protocol

from src.domain.grade.entities.subject import Subject


class GradeBookReader(Protocol):
    # @abstractmethod
    async def get_subject_by_name(self, name: str) -> Subject:
        raise NotImplementedError
