import logging

from dataclasses import dataclass
from uuid import UUID

from src.application.common.interfaces.uow import UnitOfWork
from src.application.common.transactional import transactional
from src.application.user.interfaces.persistence.repo import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import FullName, TgUserId, UserId
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler
from src.infrastructure.mediator.interface.mediator import EventMediator


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    first_name: str
    last_name: str
    telegram_id: int | None


@dataclass(frozen=True)
class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    user_repo: UserRepo
    uow: UnitOfWork
    mediator: EventMediator

    @transactional
    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserId()
        full_name = FullName(command.first_name, command.last_name)
        telegram_id = TgUserId(command.telegram_id)

        user = User.create(user_id, full_name, telegram_id)
        await self.user_repo.add_user(user)
        await self.mediator.publish(user.pull_events())
        await self.uow.commit()

        logger.info("User created", extra={"user": user})

        return user_id.to_raw()
