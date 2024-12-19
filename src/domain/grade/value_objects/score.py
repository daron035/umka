from dataclasses import dataclass

from src.domain.common.exceptions import DomainError
from src.domain.common.value_objects.base import ValueObject


MAX = 100
MIN = 0


@dataclass(eq=False)
class WrongSubjectScoreValueError(ValueError, DomainError):
    score: int


class WrongVariableValueError(WrongSubjectScoreValueError):
    @property
    def title(self) -> str:
        return f"Subject score {self.score} not in [0, 100]"


@dataclass(frozen=True)
class SubjectScore(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        if not (MIN <= self.value <= MAX):
            raise WrongVariableValueError(self.value)
