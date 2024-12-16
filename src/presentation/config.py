from dataclasses import dataclass, field

from src.infrastructure.postgres.config import PostgresConfig
from src.presentation.api.config import APIConfig
from src.presentation.bot.config import TelegramConfig


@dataclass
class Config:
    telegram: TelegramConfig
    api: APIConfig = field(default_factory=APIConfig)
    postgres_db: PostgresConfig = field(default_factory=PostgresConfig)
