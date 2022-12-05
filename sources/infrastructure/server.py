from typing import final

from blacksheep import Application as BaseServer
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from sources.infrastructure import configuration


@final
class Server(BaseServer):
    def __init__(self):
        super().__init__(
            debug=configuration.debug,
            show_error_details=configuration.debug,
        )
        self.setup_swagger()
        from .api import controllers  # noqa

    def setup_swagger(self):
        swagger = OpenAPIHandler(
            info=Info(title=configuration.name, version=configuration.version),
            anonymous_access=configuration.debug,
            ui_path=configuration.swagger_endpoint,
        )
        swagger.bind_app(self)
