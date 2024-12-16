from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.uow import UnitOfWork
from src.infrastructure.config_loader import load_config
from src.infrastructure.postgres.config import PostgresConfig
from src.infrastructure.postgres.main import PostgresManager
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
    setup_db(container)

    return container


def setup_config(container: Container) -> None:
    container.register(Config, instance=load_config(Config))
    conf: Config = container.resolve(Config)

    container.register(APIConfig, instance=conf.api)
    container.register(PostgresConfig, instance=conf.postgres_db)
    container.register(TelegramConfig, instance=conf.telegram)


def setup_db(container: Container) -> None:
    container.register(PostgresManager, scope=Scope.singleton)
    psql: PostgresManager = container.resolve(PostgresManager)
    session = psql.session_factory()

    container.register(AsyncSession, factory=lambda: session)
    container.register(SQLAlchemyUoW)
    container.register(UnitOfWork, factory=lambda: build_uow(container.resolve(SQLAlchemyUoW)))

    container.register(PgHealthCheck, PostgresHealthcheckService)
