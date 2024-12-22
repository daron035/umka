from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.application.common.interfaces.uow import UnitOfWork
from src.application.grade_book.interfaces.persistence.reader import GradeBookReader
from src.application.user.interfaces.persistence.reader import UserReader
from src.application.user.interfaces.persistence.repo import GradeBookRepo, UserRepo
from src.domain.grade.entities.grade import Grade
from src.domain.grade.value_objects.score import SubjectScore
from src.domain.user.value_objects import TgUserId
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler


if TYPE_CHECKING:
    from src.domain.grade.entities.subject import Subject
    from src.domain.user.value_objects.user_id import UserId


@dataclass(frozen=True)
class EnterGrade(Command[UUID]):
    subject: str
    score: int
    telegram_id: int


@dataclass(frozen=True)
class EnterGradeHandler(CommandHandler[EnterGrade, UUID]):
    grade_book_reader: GradeBookReader
    grade_book_repo: GradeBookRepo
    user_reader: UserReader
    user_repo: UserRepo
    uow: UnitOfWork

    async def __call__(self, command: EnterGrade) -> UUID:
        subj_score = SubjectScore(command.score)
        telegram_id = TgUserId(command.telegram_id)

        # TODO: объединить два метода в один, без reader
        await self.user_repo.exists_user_by_tg_id(telegram_id)
        user_id: UserId = await self.user_reader.get_user_by_tg_id(telegram_id)
        subject: Subject = await self.grade_book_reader.get_subject_by_name(command.subject)
        grade = Grade.create(user_id, subject, subj_score, telegram_id)
        await self.grade_book_repo.add(grade)
        await self.uow.commit()

        return user_id.to_raw()
