from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandStart

from src.presentation.bot.handlers.register_user import (
    process_first_name,
    process_last_name,
    start_register_user,
)
from src.presentation.bot.handlers.scores import finish_score, process_subject, start_enter_score, view_scores
from src.presentation.bot.handlers.start import start_handler
from src.presentation.bot.state.register import Register as RegisterState
from src.presentation.bot.state.score import Score as ScoreState


def setup_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.message.register(start_handler, CommandStart())
    dispatcher.callback_query.register(start_handler, F.data == "start")

    dispatcher.message.register(start_register_user, Command("register"))
    dispatcher.callback_query.register(start_register_user, F.data == "start_register_user")

    dispatcher.message.register(process_first_name, RegisterState.first_name)
    dispatcher.message.register(process_last_name, RegisterState.last_name)

    dispatcher.message.register(start_enter_score, Command("enter_scores"))
    dispatcher.callback_query.register(process_subject, ScoreState.subject)
    dispatcher.message.register(finish_score, ScoreState.score)

    dispatcher.message.register(view_scores, Command("view_scores"))
