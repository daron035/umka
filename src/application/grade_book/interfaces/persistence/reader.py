from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol

from src.application.grade_book.dto import GradeDTO
from src.domain.grade.entities.subject import Subject


class GradeBookReader(Protocol):
    @abstractmethod
    async def get_subject_by_name(self, name: str) -> Subject:
        raise NotImplementedError

    @abstractmethod
    async def get_grades_by_tg_id(self, tg_id: int) -> Iterable[GradeDTO]:
        raise NotImplementedError
