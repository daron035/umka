from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar


Param = ParamSpec("Param")
ReturnType = TypeVar("ReturnType")


def transactional(
    func: Callable[Param, Coroutine[Any, Any, ReturnType]],
) -> Callable[Param, Coroutine[Any, Any, ReturnType]]:
    @wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> ReturnType:
        uow = getattr(args[0], "uow", None)
        if uow is None:
            raise AttributeError("The object does not have an 'uow' attribute")

        try:
            result = await func(*args, **kwargs)
            await uow.commit()
            return result
        except Exception:
            await uow.rollback()
            raise
        finally:
            await uow.close()

    return wrapped
