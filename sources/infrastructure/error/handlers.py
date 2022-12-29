from blacksheep import Request, Response, not_found, pretty_json, unauthorized
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from ..exceptions import (
    InvalidCredentialsError,
    UnprocessableError,
)
from sources.infrastructure.server import Server


""" Be careful, in this file, functions whose name contains `handler` are reserved. """


async def validation_handler(
    server: Server,
    request: Request,
    exception: UnprocessableError,
) -> Response:
    return pretty_json(status=422, data=exception.content)


async def not_found_handler(
    server: Server,
    request: Request,
    exception: ObjectDoesNotExist,
) -> Response:
    return not_found()


async def invalid_credentials_handler(
    server: Server,
    request: Request,
    exception: InvalidCredentialsError,
) -> Response:
    return unauthorized("Invalid credentials.")


async def conflict_handler(
    server: Server,
    request: Request,
    exception: IntegrityError,
) -> Response:
    return Response(409)
