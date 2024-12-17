from typing import NoReturn

from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user.exceptions import UserIdAlreadyExistsError
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user import entities
from src.domain.user.value_objects import TgUserId
from src.infrastructure.postgres.converters import (
    convert_user_entity_to_db_model,
)
from src.infrastructure.postgres.exception_mapper import exception_mapper
from src.infrastructure.postgres.models.user import User
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def add_user(self, user: entities.User) -> None:
        db_user = convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
        user: User | None = await self._session.scalar(select(User).where(User.telegram_id == tg_user_id.to_raw()))
        return user is not None

    def _parse_error(self, err: DBAPIError, user: entities.User) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case _:
                raise RepoError from err
