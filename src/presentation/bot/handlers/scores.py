from aiogram import types
from aiogram.fsm.context import FSMContext

from src.application.grade_book.commands.enter_grade import EnterGrade
from src.infrastructure.containers import get_container
from src.infrastructure.mediator.mediator import MediatorImpl
from src.presentation.bot.messages.score import ScoreBuilder
from src.presentation.bot.state.score import Score as ScoreState
from src.presentation.bot.utils import callback_handler_wrapper


@callback_handler_wrapper
async def start_enter_score(message: types.Message, state: FSMContext) -> None:
    content = ScoreBuilder().build()
    await message.answer(**content)
    await state.set_state(ScoreState.subject)


async def process_subject(message: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(subject=message.data)

    await message.answer(f"Введите баллы по предмету: {message.data}")
    await state.set_state(ScoreState.score)


async def finish_score(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(score=int(message.text))
    subject = data.get("subject")
    # score = data.get("score") NONE
    score = int(message.text)
    telegram_id = message.from_user.id

    mediator: MediatorImpl = get_container().resolve(MediatorImpl)
    await mediator.send(EnterGrade(subject, score, telegram_id))

    await message.answer(f"{subject}: {message.text}")
    await state.clear()
