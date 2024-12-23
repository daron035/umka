from collections.abc import Iterable

from sqlalchemy import select

from src.application.grade_book.dto import GradeDTO
from src.application.grade_book.exceptions import SubjectExistError
from src.application.grade_book.interfaces.persistence.reader import GradeBookReader
from src.application.user.interfaces.persistence.repo import GradeBookRepo
from src.domain.grade.entities import GradeEntity, SubjectEntity
from src.infrastructure.postgres.converters import (
    convert_db_model_to_grade_dto,
    convert_db_model_to_subject_entity,
    convert_grade_entity_to_db_model,
)
from src.infrastructure.postgres.exception_mapper import exception_mapper
from src.infrastructure.postgres.models import GradeModel, SubjectModel, UserModel
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo


class GradeBookReaderImpl(SQLAlchemyRepo, GradeBookReader):
    @exception_mapper
    async def get_subject_by_name(self, name: str) -> SubjectEntity:
        stmt = select(SubjectModel).where(SubjectModel.name == name)
        subject: SubjectModel | None = await self._session.scalar(stmt)
        if subject is None:
            raise SubjectExistError(name)

        return convert_db_model_to_subject_entity(subject)

    @exception_mapper
    async def get_grades_by_tg_id(self, tg_id: int) -> Iterable[GradeDTO]:
        query = (
            select(GradeModel, SubjectModel)
            .join(UserModel, UserModel.id == GradeModel.user_id)
            .join(SubjectModel, SubjectModel.id == GradeModel.subject_id)
            .where(UserModel.telegram_id == tg_id)
        )
        result = await self._session.execute(query)
        # TODO: yield
        grades = [convert_db_model_to_grade_dto(grade, subject) for grade, subject in result]

        return grades


class GradeBookRepoImpl(SQLAlchemyRepo, GradeBookRepo):
    @exception_mapper
    async def add(self, grade: GradeEntity) -> None:
        db_grade = convert_grade_entity_to_db_model(grade)
        self._session.add(db_grade)
        await self._session.flush((db_grade,))
