from aiohttp.web import Request, Response, RouteTableDef, json_response


healthcheck_router = RouteTableDef()


@healthcheck_router.get("/")
async def heathcheck_view(request: Request) -> Response:
    return json_response({"status": "ok"})
