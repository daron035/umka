import inspect

from collections.abc import Awaitable, Callable

from aiogram import types
from aiogram.fsm.context import FSMContext


HandlerFuncType = Callable[[types.Message | types.CallbackQuery, FSMContext | None], Awaitable[None]]
MessageHandlerFuncType = Callable[[types.Message], Awaitable[None]]


def callback_handler_wrapper(handler: HandlerFuncType) -> MessageHandlerFuncType:
    async def wrapped(event: types.Message | types.CallbackQuery, state: FSMContext | None = None) -> None:
        if isinstance(event, types.Message):
            message = event
        elif isinstance(event, types.CallbackQuery):
            message = event.message

        handler_signature = inspect.signature(handler)
        if "state" in handler_signature.parameters:
            await handler(message, state)
        else:
            await handler(message)

        if isinstance(event, types.CallbackQuery):
            await event.answer()
            await message.delete()

    return wrapped
