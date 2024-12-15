from aiohttp.web import RouteTableDef, Request, Response, json_response


healthcheck_router = RouteTableDef()


@healthcheck_router.get("/")
async def heathcheck_view(request: Request) -> Response:
    return json_response({"status": "ok"})
