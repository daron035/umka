from aiohttp.web import Application

from .healthcheck import healthcheck_router


def setup_controllers(app: Application) -> None:
    app.add_routes(healthcheck_router)
