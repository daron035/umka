from aiogram import types
from aiogram.fsm.context import FSMContext

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
    subject = data.get("subject")
    await state.update_data(score=message.text)
    await message.answer(f"{subject}: {message.text}")
    await state.clear()
