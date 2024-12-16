from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.presentation.bot.messages.base import BaseMessageBuilder


class StartMessageBuilder(BaseMessageBuilder):
    _text = (
        "Привет! 👋 \n\n"
        "Добро пожаловать в наш бот! Мы рады видеть тебя здесь. Чтобы продолжить, выбери одно из действий:"
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1️⃣ Зарегистрироваться", callback_data="start_register_user")],
        ],
    )
