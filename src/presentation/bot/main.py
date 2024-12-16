from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiohttp.web import Application

from src.infrastructure.containers import get_container
from src.presentation.bot.config import TelegramConfig
from src.presentation.bot.handlers.register_user import process_first_name, process_last_name, start_register_user
from src.presentation.bot.handlers.start import start_handler
from src.presentation.bot.state.register import Register as RegisterState
from src.presentation.bot.views import TelegramWebhookView
from src.presentation.config import Config


def add_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.message.register(start_handler, CommandStart())
    dispatcher.callback_query.register(start_handler, F.data == "start")

    dispatcher.message.register(start_register_user, Command("register"))
    dispatcher.callback_query.register(start_register_user, F.data == "start_register_user")

    dispatcher.message.register(process_first_name, RegisterState.first_name)
    dispatcher.message.register(process_last_name, RegisterState.last_name)


async def telegram_view_factory(config: TelegramConfig) -> TelegramWebhookView:
    bot = Bot(token=config.TELEGRAM_API_KEY)
    await bot.set_webhook(config.telegram_web_hook)

    dispatcher = Dispatcher()
    add_handlers(dispatcher)

    return TelegramWebhookView(dispatcher=dispatcher, bot=bot)


async def setup_tg_router(app: Application) -> None:
    config: TelegramConfig = get_container().resolve(Config).telegram  # type: ignore

    app.router.add_route(
        "*",
        config.TELEGRAM_WEBHOOK_PATH,
        await telegram_view_factory(config),
        name="tg_webhook_handler",
    )
