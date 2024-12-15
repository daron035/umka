from aiohttp.web import Application

from .general import general_router


def setup_controllers(app: Application) -> None:
    app.add_routes(general_router)
