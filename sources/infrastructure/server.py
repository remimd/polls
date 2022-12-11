from __future__ import annotations

import inspect
from typing import Callable, Type, final

from blacksheep import Application as BaseServer, Request, Response
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
        self.setup_error_handlers()

    @staticmethod
    def is_error_handler(function: _ErrorHandler) -> bool:
        return inspect.isfunction(function) and "handler" in function.__name__

    def add_error_handler(self, exception: Type[BaseException], handler: _ErrorHandler):
        self.exceptions_handlers[exception] = handler

    def setup_error_handlers(self):
        from . import error_handlers

        handlers = inspect.getmembers(error_handlers, self.is_error_handler)

        for _, handler in handlers:
            signature = inspect.signature(handler)
            parameter = tuple(signature.parameters.values())[2]
            exception = parameter.annotation

            if not issubclass(exception, BaseException):
                raise TypeError(f"`{exception.__name__}` isn't a valid exception.")

            self.add_error_handler(exception, handler)

    def setup_swagger(self):
        swagger = OpenAPIHandler(
            info=Info(title=configuration.name, version=configuration.version),
            anonymous_access=configuration.debug,
            ui_path=configuration.swagger_endpoint,
        )
        swagger.bind_app(self)


_ErrorHandler = Callable[[Server, Request, BaseException], Response]
