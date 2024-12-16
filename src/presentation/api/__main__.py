import asyncio

from typing import TYPE_CHECKING

import anyio

from aiohttp import web

from src.infrastructure.config_loader import load_config
from src.presentation.api.main import init_app
from src.presentation.config import Config


if TYPE_CHECKING:
    from src.presentation.api.config import APIConfig


async def main() -> None:
    app = await init_app()
    config: Config = load_config(Config)
    api_config: APIConfig = config.api

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, api_config.host, api_config.port)
    await site.start()

    await anyio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
