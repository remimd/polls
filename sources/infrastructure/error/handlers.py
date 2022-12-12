from blacksheep import Request, Response, not_found, pretty_json
from django.core.exceptions import ObjectDoesNotExist

from sources.infrastructure.error.exceptions import UnprocessableError
from sources.infrastructure.server import Server


""" Be careful, in this file, functions whose name contains `handler` are reserved. """


async def validation_handler(
    server: Server,
    request: Request,
    exception: UnprocessableError,
) -> Response:
    return pretty_json(status=422, data=exception.errors)


async def not_found_handler(
    server: Server,
    request: Request,
    exception: ObjectDoesNotExist,
) -> Response:
    return not_found()
