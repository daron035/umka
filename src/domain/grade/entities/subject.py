from dataclasses import (
    dataclass,
)
from typing import Self

from src.domain.common.entities import Entity


@dataclass
class Subject(Entity):
    oid: int
    name: str
    description: str | None

    @classmethod
    def create(
        cls,
        oid: int,
        name: str,
        description: str | None,
    ) -> Self:
        return cls(oid, name, description)
