from blacksheep import Application, Request, Response, not_found, pretty_json
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from sources.infrastructure.exceptions import APIError


""" Be careful, in this file, functions whose name contains `handler` are reserved. """


async def api_error_handler(
    application: Application,
    request: Request,
    exception: APIError,
) -> Response:
    return pretty_json(status=exception.status_code, data=exception.content)


async def not_found_handler(
    application: Application,
    request: Request,
    exception: ObjectDoesNotExist,
) -> Response:
    return not_found()


async def conflict_handler(
    application: Application,
    request: Request,
    exception: IntegrityError,
) -> Response:
    return Response(409)
