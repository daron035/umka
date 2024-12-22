from aiohttp.web import Request, Response, RouteTableDef, json_response

from src.infrastructure.containers import get_container
from src.infrastructure.postgres.services.healthcheck import PgHealthCheck


general_router = RouteTableDef()


@general_router.get("/")
async def heathcheck_view(request: Request) -> Response:
    return json_response({"status": "ok"})


@general_router.get("/test-pg-connection")
async def test_postgres_db(request: Request) -> Response:
    psql: PgHealthCheck = get_container().resolve(PgHealthCheck)

    response = await psql.check()
    return json_response(response)
