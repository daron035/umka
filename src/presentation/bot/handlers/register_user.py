from aiogram import types
from aiogram.fsm.context import FSMContext

from src.application.user.commands.create_user import CreateUser
from src.infrastructure.containers import get_container
from src.infrastructure.mediator.mediator import MediatorImpl
from src.presentation.bot.state.register import Register as RegisterState
from src.presentation.bot.utils import callback_handler_wrapper


@callback_handler_wrapper
async def start_register_user(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите ваше имя:")
    await state.set_state(RegisterState.first_name)


@callback_handler_wrapper
async def process_first_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegisterState.last_name)


@callback_handler_wrapper
async def process_last_name(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = message.text

    mediator: MediatorImpl = get_container().resolve(MediatorImpl)
    user = CreateUser(first_name, last_name, message.from_user.id)

    try:
        await mediator.send(user)
    except:
        await message.answer("Что-то пошло не так, попробуйте с начала.")
        await start_register_user(message)
        return

    await message.answer(f"Регистрация завершена! 🎉\nИмя: {first_name}\nФамилия: {last_name}")
    await state.clear()
