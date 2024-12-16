from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiohttp.web import Application

from src.infrastructure.containers import get_container
from src.presentation.bot.config import TelegramConfig
from src.presentation.bot.handlers.start import start_handler
from src.presentation.bot.views import TelegramWebhookView
from src.presentation.config import Config


async def telegram_view_factory(config: TelegramConfig) -> TelegramWebhookView:
    bot = Bot(token=config.TELEGRAM_API_KEY)
    await bot.set_webhook(config.telegram_web_hook)

    dispatcher = Dispatcher()
    dispatcher.message.register(start_handler, CommandStart())

    return TelegramWebhookView(dispatcher=dispatcher, bot=bot)


async def setup_tg_router(app: Application) -> None:
    config: TelegramConfig = get_container().resolve(Config).telegram  # type: ignore

    app.router.add_route(
        "*",
        config.TELEGRAM_WEBHOOK_PATH,
        await telegram_view_factory(config),
        name="tg_webhook_handler",
    )
