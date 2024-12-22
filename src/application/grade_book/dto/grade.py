from dataclasses import dataclass

from src.application.common.dto import DTO


@dataclass(frozen=True)
class Grade(DTO):
    id: int
    name: str
    score: int
