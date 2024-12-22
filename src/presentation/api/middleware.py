from collections.abc import Awaitable, Callable

from aiohttp.web import Request, Response, middleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.exceptions import SessionCloseError
from src.infrastructure.containers import get_container


@middleware
async def db_session(request: Request, handler: Callable[[Request], Awaitable[Response]]) -> Response:
    resp = await handler(request)
    try:
        await get_container().resolve(AsyncSession).close()  # type: ignore
    except SQLAlchemyError as err:
        raise SessionCloseError from err
    return resp
