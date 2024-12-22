import orjson

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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

        self.session_factory = async_sessionmaker(
            bind=self._async_engine,
            autoflush=False,
            expire_on_commit=False,
        )
        self.read_only_session_factory = async_sessionmaker(
            bind=self._read_only_async_engine,
            autoflush=False,
            expire_on_commit=False,
        )
