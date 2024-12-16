from aiohttp import web

from src.presentation.api.controllers.main import setup_controllers
from src.presentation.bot.main import setup_tg_router


async def init_app() -> web.Application:
    app = web.Application()

    setup_controllers(app)
    await setup_tg_router(app)

    return app


async def run_app(app: web.Application) -> None:
    web.run_app(app, port=8000)
