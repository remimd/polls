from blacksheep import Request, Response, pretty_json

from common.exceptions import UnprocessableError
from sources.infrastructure.server import Server


""" Be careful, in this file, functions whose name contains `handler` are reserved. """


async def validation_handler(
    server: Server,
    request: Request,
    exception: UnprocessableError,
) -> Response:
    return pretty_json(status=422, data=exception.errors)
