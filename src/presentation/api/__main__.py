import asyncio
from aiohttp import web

from src.presentation.api.main import init_app


async def main() -> None:
    app = init_app()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8000)
    await site.start()

    while True:
        await asyncio.sleep(3600)  # sleep forever


if __name__ == "__main__":
    asyncio.run(main())
