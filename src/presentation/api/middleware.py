from collections.abc import Awaitable, Callable

import structlog

from aiohttp.web import Request, Response, middleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from src.application.common.exceptions import SessionCloseError
from src.infrastructure.containers import get_container


@middleware
async def structlog_bind(
    request: Request,
    handler: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.get("request_id", "unknown")
    with structlog.contextvars.bound_contextvars(request_id=str(request_id)):
        return await handler(request)


@middleware
async def db_session(request: Request, handler: Callable[[Request], Awaitable[Response]]) -> Response:
    request["request_id"] = uuid7()
    resp = await handler(request)
    try:
        await get_container().resolve(AsyncSession).close()  # type: ignore
    except SQLAlchemyError as err:
        raise SessionCloseError from err
    return resp
