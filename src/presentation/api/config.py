from dataclasses import dataclass, field

from src.infrastructure.postgres.config import PostgresConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = __debug__


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    postgres_db: PostgresConfig = field(default_factory=PostgresConfig)
