import logging

from src.infrastructure.log.config import LoggingConfig


def configure_logging(cfg: LoggingConfig) -> None:
    logging.basicConfig(level=cfg.level)
