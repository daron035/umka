from aiogram import types

from src.presentation.bot.messages.start import StartMessageBuilder
from src.presentation.bot.utils import callback_handler_wrapper


@callback_handler_wrapper
async def start_handler(message: types.Message) -> None:
    content = StartMessageBuilder().build()
    await message.answer(**content)
