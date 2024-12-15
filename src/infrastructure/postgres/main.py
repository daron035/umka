from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import orjson

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.postgres.config import PostgresConfig


class PostgresManager:
    def __init__(self, db_config: PostgresConfig):
        self._db_config = db_config
        self._async_engine = create_async_engine(
            self._db_config.full_url,
            echo=True,
            echo_pool=self._db_config.echo,
            json_serializer=lambda data: orjson.dumps(data).decode(),
            json_deserializer=orjson.loads,
            pool_size=50,
            isolation_level="READ COMMITTED",
        )
        self._read_only_async_engine = create_async_engine(
            self._db_config.full_url,
            echo=True,
            echo_pool=self._db_config.echo,
            json_serializer=lambda data: orjson.dumps(data).decode(),
            json_deserializer=orjson.loads,
            pool_size=50,
            isolation_level="AUTOCOMMIT",
        )
        self.read_only_session_factory = async_sessionmaker(
            bind=self._read_only_async_engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self.session_factory = async_sessionmaker(bind=self._async_engine, autoflush=False, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @asynccontextmanager
    async def get_read_only_session(self) -> AsyncGenerator[AsyncSession]:
        session: AsyncSession = self.read_only_session_factory()
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await session.close()
