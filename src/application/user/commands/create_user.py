from dataclasses import dataclass
from uuid import UUID

from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence.repo import UserRepo
from src.domain.user.entities import UserEntity
from src.domain.user.value_objects import FullName, TgUserId, UserId
from src.infrastructure.mediator.interface.entities.command import Command
from src.infrastructure.mediator.interface.handlers.command import CommandHandler
from src.infrastructure.mediator.interface.mediator import EventMediator


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    first_name: str
    last_name: str
    telegram_id: int


@dataclass(frozen=True)
class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    user_repo: UserRepo
    uow: UnitOfWork
    mediator: EventMediator

    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserId()
        full_name = FullName(command.first_name, command.last_name)
        tg_user_id = TgUserId(command.telegram_id)

        exists = await self.user_repo.exists_user_by_tg_id(tg_user_id)
        user = UserEntity.create(user_id, full_name, tg_user_id, exists)
        await self.user_repo.add_user(user)
        await self.mediator.publish(user.pull_events())
        await self.uow.commit()

        return user_id.to_raw()
