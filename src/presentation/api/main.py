from aiohttp import web

from src.presentation.api.controllers.main import setup_controllers
from src.presentation.api.middleware import db_session, structlog_bind
from src.presentation.bot.main import setup_tg_router


async def init_app() -> web.Application:
    app = web.Application(middlewares=[db_session, structlog_bind])

    setup_controllers(app)
    await setup_tg_router(app)

    return app


async def run_app(app: web.Application) -> None:
    web.run_app(app, port=8000)
