from typing import Any, ClassVar

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Subject(BaseModel):
    __tablename__ = "subjects"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(default=None, server_default=sa.Null())
