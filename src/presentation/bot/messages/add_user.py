from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.presentation.bot.messages.base import BaseMessageBuilder


class AddUserMessageBuilder(BaseMessageBuilder):
    _text = "Введите пожалуйста имя и фамилию"
    _reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить", callback_data="start")],
        ],
        one_time_keyboard=True,
    )
