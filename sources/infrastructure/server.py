from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info

from sources.infrastructure.configurations import configuration


class Server(Application):
    def __init__(self):
        debug = configuration.debug
        super().__init__(debug=debug, show_error_details=debug)
        self._setup_swagger()
        from .api import controllers  # noqa

    def _setup_swagger(self):
        swagger = OpenAPIHandler(
            info=Info(title=configuration.name, version=configuration.version),
            anonymous_access=self.debug,
            ui_path=configuration.documentation_endpoint,
        )
        swagger.bind_app(self)


server = Server()
server_path = f"{globals()['__name__']}:server"
