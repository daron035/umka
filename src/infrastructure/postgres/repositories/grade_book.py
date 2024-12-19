from sqlalchemy import select

from src.application.grade_book.interfaces.persistence.reader import GradeBookReader
from src.application.user.interfaces.persistence.repo import GradeBookRepo
from src.domain.grade.entities import GradeEntity, SubjectEntity
from src.infrastructure.postgres.converters import (
    convert_db_model_to_subject_entity,
    convert_grade_entity_to_db_model,
)
from src.infrastructure.postgres.exception_mapper import exception_mapper
from src.infrastructure.postgres.models import SubjectModel
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo


class GradeBookReaderImpl(SQLAlchemyRepo, GradeBookReader):
    @exception_mapper
    async def get_subject_by_name(self, name: str) -> SubjectEntity:
        stmt = select(SubjectModel).where(SubjectModel.name == name)
        subject: SubjectModel | None = await self._session.scalar(stmt)
        if subject is None:
            # raise SubjectExistError(name)
            raise Exception

        return convert_db_model_to_subject_entity(subject)


class GradeBookRepoImpl(SQLAlchemyRepo, GradeBookRepo):
    @exception_mapper
    async def add(self, grade: GradeEntity) -> None:
        db_grade = convert_grade_entity_to_db_model(grade)
        self._session.add(db_grade)
        await self._session.flush((db_grade,))
