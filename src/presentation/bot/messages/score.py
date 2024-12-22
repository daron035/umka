from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.presentation.bot.messages.base import BaseMessageBuilder


# class ScoreBuilder(BaseMessageBuilder):
#     _text = "Выберите один из предметов"
#     subjects = ["Математика", "Русский язык", "Физика", "Химия", "Информатика"]
#     _reply_markup = InlineKeyboardMarkup(
#         inline_keyboard=[[InlineKeyboardButton(text=subject, callback_data=subject)] for subject in subjects],
#     )


# class ScoreBuilder(BaseMessageBuilder):
#     _text = "Выберите один из предметов"
#     subjects = ["Математика", "Русский язык", "Физика", "Химия", "Информатика"]
#     builder = InlineKeyboardBuilder()
#     builder.row(
#         InlineKeyboardButton(text=subjects[0], callback_data=subjects[0]),
#         InlineKeyboardButton(text=subjects[1], callback_data=subjects[1]),
#     )
#     builder.row(
#         InlineKeyboardButton(text=subjects[2], callback_data=subjects[2]),
#         InlineKeyboardButton(text=subjects[3], callback_data=subjects[3]),
#     )
#     builder.row(
#         InlineKeyboardButton(text=subjects[4], callback_data=subjects[4]),
#         InlineKeyboardButton(text=subjects[5], callback_data=subjects[5]),
#     )
#     _reply_markup = builder.as_markup()


class ScoreBuilder(BaseMessageBuilder):
    _text = "Выберите один из предметов"
    _subjects = ["Математика", "Русский язык", "Физика", "Химия", "Информатика"]

    def __init__(self):
        self.builder = InlineKeyboardBuilder()

        rows = [self._subjects[i : i + 2] for i in range(0, len(self._subjects), 2)]
        for row in rows:
            self.builder.row(*[InlineKeyboardButton(text=subject, callback_data=subject) for subject in row])

        self._reply_markup = self.builder.as_markup()


class ViewGradesBuilder(BaseMessageBuilder):
    def __init__(self, grades: list) -> None:
        if grades:
            result = "\n".join(f"{grade.name} — {grade.score}" for grade in grades)
        else:
            result = "Пока пусто - воспользуйтесь командой /enter_scores"
        self._text = result
