from collections.abc import Iterable
from dataclasses import dataclass

from src.application.grade_book.dto import GradeDTO
from src.application.grade_book.interfaces.persistence.reader import GradeBookReader
from src.domain.user.value_objects.tg_user_id import TgUserId
from src.infrastructure.mediator.interface.entities.query import Query
from src.infrastructure.mediator.interface.handlers.query import QueryHandler


@dataclass(frozen=True)
class GetGradesByTgId(Query[Iterable[GradeDTO]]):
    tg_id: int


@dataclass(frozen=True)
class GetGradesByTgIdHandler(QueryHandler[GetGradesByTgId, Iterable[GradeDTO]]):
    grade_book_reader: GradeBookReader

    async def __call__(self, command: GetGradesByTgId) -> Iterable[GradeDTO]:
        tg_id = TgUserId(command.tg_id)

        grades = await self.grade_book_reader.get_grades_by_tg_id(tg_id.to_raw())
        return grades
