from typing import NoReturn
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.application.common.exceptions import RepoError
from src.application.user.exceptions import UserIdAlreadyExistsError, UserIdNotExistError
from src.application.user.interfaces.persistence import UserRepo
from src.application.user.interfaces.persistence.reader import UserReader
from src.domain.user.entities import UserEntity
from src.domain.user.value_objects import TgUserId
from src.domain.user.value_objects.user_id import UserId
from src.infrastructure.postgres.converters import (
    convert_user_entity_to_db_model,
)
from src.infrastructure.postgres.exception_mapper import exception_mapper
from src.infrastructure.postgres.models import UserModel
from src.infrastructure.postgres.repositories.base import SQLAlchemyRepo


class UserReaderImpl(SQLAlchemyRepo, UserReader):
    @exception_mapper
    async def get_user_by_tg_id(self, telegram_id: TgUserId) -> UserId:
        stmt = select(UserModel.id).where(UserModel.telegram_id == telegram_id.to_raw())
        user_id: UUID | None = await self._session.scalar(stmt)
        if user_id is None:
            raise UserIdNotExistError(telegram_id.to_raw())

        return UserId(user_id)


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @exception_mapper
    async def add_user(self, user: UserEntity) -> None:
        db_user = convert_user_entity_to_db_model(user)
        self._session.add(db_user)
        try:
            await self._session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, user)

    @exception_mapper
    async def exists_user_by_tg_id(self, tg_user_id: TgUserId) -> bool:
        # user: UserModel | None = await self._session.scalar(select(UserModel).where(UserModel.telegram_id == tg_user_id.to_raw()))
        # return user is not None

        stmt = select(exists().where(UserModel.telegram_id == tg_user_id.to_raw()))
        result = await self._session.scalar(stmt)
        return bool(result)

    def _parse_error(self, err: DBAPIError, user: UserEntity) -> NoReturn:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_raw()) from err
            case _:
                raise RepoError from err
