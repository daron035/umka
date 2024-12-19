from dataclasses import (
    dataclass,
)
from typing import Self

from src.domain.common.entities.aggregate_root import AggregateRoot
from src.domain.grade.value_objects.score import SubjectScore
from src.domain.user.value_objects import TgUserId, UserId

from .subject import Subject


@dataclass
class Grade(AggregateRoot):
    user_id: UserId
    subject: Subject
    score: SubjectScore
    telegram_id: TgUserId

    @classmethod
    def create(
        cls,
        user_id: UserId,
        subject: Subject,
        score: SubjectScore,
        telegram_id: TgUserId,
    ) -> Self:
        grade = cls(user_id, subject, score, telegram_id)
        # TODO: record event
        return grade
