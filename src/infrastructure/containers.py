from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.commands.create_user import CreateUser, CreateUserHandler
from src.application.user.interfaces.persistence.repo import UserRepo
from src.infrastructure.config_loader import load_config
from src.infrastructure.mediator.mediator import MediatorImpl
from src.infrastructure.postgres.config import PostgresConfig
from src.infrastructure.postgres.main import PostgresManager
from src.infrastructure.postgres.repositories.user import UserRepoImpl
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck, PostgresHealthcheckService
from src.infrastructure.postgres.uow import SQLAlchemyUoW
from src.infrastructure.uow import build_uow
from src.presentation.api.config import APIConfig
from src.presentation.bot.config import TelegramConfig
from src.presentation.config import Config


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    setup_config(container)
    setup_repositories(container)
    container.register(MediatorImpl, factory=lambda: setup_mediator(container))
    setup_db(container)

    return container


def setup_config(container: Container) -> None:
    container.register(Config, instance=load_config(Config))
    conf: Config = container.resolve(Config)

    container.register(APIConfig, instance=conf.api)
    container.register(PostgresConfig, instance=conf.postgres_db)
    container.register(TelegramConfig, instance=conf.telegram)


def setup_mediator(container: Container) -> MediatorImpl:
    mediator = MediatorImpl()

    create_user_handler = CreateUserHandler(
        user_repo=container.resolve(UserRepo),
        uow=container.resolve(UnitOfWork),
        mediator=mediator,
    )

    mediator.register_command_handler(CreateUser, create_user_handler)

    return mediator


def setup_repositories(container: Container) -> None:
    container.register(UserRepo, UserRepoImpl)


def setup_db(container: Container) -> None:
    container.register(PostgresManager, scope=Scope.singleton)
    psql: PostgresManager = container.resolve(PostgresManager)
    session = psql.session_factory()

    container.register(AsyncSession, factory=lambda: session)
    container.register(SQLAlchemyUoW)
    container.register(UnitOfWork, factory=lambda: build_uow(container.resolve(SQLAlchemyUoW)))

    container.register(PgHealthCheck, PostgresHealthcheckService)
