from typing import Protocol

from src.domain.grade.entities.grade import Grade


class GradeBookRepo(Protocol):
    async def enter_grades(self, grade: Grade) -> None:
        raise NotImplementedError
