import logging

from src.infrastructure.log.config import LoggingConfig


# TODO: configure_logging
def configure_logging(cfg: LoggingConfig) -> None:
    logging.basicConfig(level=cfg.level)
