from collections.abc import Awaitable, Callable

from aiogram import types


HandlerFuncType = Callable[[types.Message | types.CallbackQuery], Awaitable[None]]
MessageHandlerFuncType = Callable[[types.Message], Awaitable[None]]


def callback_handler_wrapper(handler: HandlerFuncType) -> MessageHandlerFuncType:
    async def wrapped(event: types.Message | types.CallbackQuery) -> None:
        if isinstance(event, types.Message):
            message = event
        elif isinstance(event, types.CallbackQuery):
            message = event.message

        await handler(message)

        if isinstance(event, types.CallbackQuery):
            await message.delete()

    return wrapped
