from aiohttp import web

from src.presentation.api.controllers.main import setup_controllers


def init_app() -> web.Application:
    app = web.Application()

    setup_controllers(app)

    return app


async def run_app(app: web.Application) -> None:
    web.run_app(app, port=8000)
