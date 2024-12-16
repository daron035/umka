from dataclasses import dataclass


@dataclass
class TelegramConfig:
    TELEGRAM_API_KEY: str
    TELEGRAM_WEBHOOK_HOST: str
    TELEGRAM_WEBHOOK_PATH: str

    @property
    def telegram_web_hook(self) -> str:
        return f"{self.TELEGRAM_WEBHOOK_HOST}{self.TELEGRAM_WEBHOOK_PATH}"
