import asyncio

import anyio

from aiohttp import web

from src.presentation.api.main import init_app


async def main() -> None:
    app = init_app()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

    await anyio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
