from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TimedBaseModel


class Grade(TimedBaseModel):
    __tablename__ = "grades"
    __mapper_args__: ClassVar[dict[Any, Any]] = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship()
