from aiohttp.web import run_app

from src.presentation.api.main import init_app


if __name__ == "__main__":
    run_app(init_app(), port=8000)
