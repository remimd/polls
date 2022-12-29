import inspect
from typing import Callable, Type

from blacksheep import Application, Request, Response
from blacksheep.server.openapi.v3 import OpenAPIHandler
from guardpost.common import AuthenticatedRequirement, Policy
from openapidocs.v3 import Info

from sources.infrastructure import configuration


_ErrorHandler = Callable[[Application, Request, BaseException], Response]


class APIComponent:
    def __init__(self):
        from sources.infrastructure.server import application

        self.application = application

    def setup(self):
        self._setup_swagger()
        self._setup_authorizations()
        self._setup_error_handlers()
        self._setup_controllers()

    @staticmethod
    def _setup_controllers():
        from .controllers import access_controller  # noqa
        from .controllers import poll_controller  # noqa

    def _setup_error_handlers(self):
        from . import error_handlers

        members = inspect.getmembers(error_handlers, self._is_error_handler)

        for _, function in members:
            signature = inspect.signature(function)
            parameter = tuple(signature.parameters.values())[2]
            exception = parameter.annotation

            if not issubclass(exception, BaseException):
                raise TypeError(f"`{exception.__name__}` isn't a valid exception.")

            self._add_error_handler(exception, function)

    def _setup_swagger(self):
        swagger = OpenAPIHandler(
            info=Info(title=configuration.name, version=configuration.version),
            anonymous_access=configuration.debug,
            ui_path=configuration.swagger_endpoint,
        )
        swagger.bind_app(self.application)

    def _setup_authorizations(self):
        from .authentication.handlers import JWTHandler

        authentication = self.application.use_authentication()
        authentication.add(
            JWTHandler(),
        )

        authorization = self.application.use_authorization()
        authorization.default_policy = Policy(
            "authenticated",
            AuthenticatedRequirement(),
        )

    @staticmethod
    def _is_error_handler(function: _ErrorHandler) -> bool:
        return inspect.isfunction(function) and "handler" in function.__name__

    def _add_error_handler(
        self,
        exception: Type[BaseException],
        handler: _ErrorHandler,
    ):
        self.application.exceptions_handlers[exception] = handler
