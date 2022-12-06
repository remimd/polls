from typing import final

from blacksheep import Application as BaseServer, Response, pretty_json
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from common.exceptions import UnprocessableError
from sources.infrastructure import configuration


@final
class Server(BaseServer):
    def __init__(self):
        super().__init__(
            debug=configuration.debug,
            show_error_details=configuration.debug,
        )

        self.setup_swagger()
        self.setup_error_handlers()
        self.setup_imports()

    def setup_error_handlers(self):
        self.exceptions_handlers[UnprocessableError] = validation_handler

    def setup_swagger(self):
        swagger = OpenAPIHandler(
            info=Info(title=configuration.name, version=configuration.version),
            anonymous_access=configuration.debug,
            ui_path=configuration.swagger_endpoint,
        )
        swagger.bind_app(self)

    @staticmethod
    def setup_imports():
        from .django import asgi  # noqa
        from .api import controllers  # noqa


async def validation_handler(self, request, exc: UnprocessableError) -> Response:
    assert isinstance(exc, UnprocessableError)
    return pretty_json(status=422, data=exc.errors)
