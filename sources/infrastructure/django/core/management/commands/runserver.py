import inspect
import ssl

import click
import uvicorn
from django.core.management import CommandParser
from django.core.management.commands.runserver import Command as BaseRunServerCommand
from h11._connection import DEFAULT_MAX_INCOMPLETE_EVENT_SIZE
from uvicorn.config import SSL_PROTOCOL_VERSION
from uvicorn.main import (
    HTTP_CHOICES,
    INTERFACE_CHOICES,
    LEVEL_CHOICES,
    LIFESPAN_CHOICES,
    LOOP_CHOICES,
    WS_CHOICES,
)

from sources.infrastructure.configurations import configuration
from sources.infrastructure.server import server_path


class Command(BaseRunServerCommand):
    ALLOWED_IPS = ";".join(configuration.allowed_hosts)
    DEBUG = configuration.debug
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 8000

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "-H",
            "--host",
            default=self.DEFAULT_HOST,
            help="Bind socket to this host.",
        )
        parser.add_argument(
            "-p",
            "--port",
            default=self.DEFAULT_PORT,
            type=int,
            help="Bind socket to this port.",
        )
        parser.add_argument(
            "--uds",
            help="Bind to a UNIX domain socket.",
        )
        parser.add_argument(
            "--fd",
            type=int,
            help="Bind to socket from this file descriptor.",
        )
        parser.add_argument(
            "-r",
            "--reload",
            action="store_true",
            help="Enable auto-reload.",
        )
        parser.add_argument(
            "--reload-dir",
            nargs="*",
            type=click.Path(exists=True),
            help="Set reload directories explicitly, instead of using the current working directory.",
            dest="reload_dirs",
        )
        parser.add_argument(
            "--reload-include",
            nargs="*",
            help="Set glob patterns to include while watching for files. Includes '*.py' "
            "by default; these defaults can be overridden with `--reload-exclude`. "
            "This option has no effect unless watchfiles is installed.",
            dest="reload_includes",
        )
        parser.add_argument(
            "--reload-exclude",
            nargs="*",
            help="Set glob patterns to exclude while watching for files. Includes "
            "'.*, .py[cod], .sw.*, ~*' by default; these defaults can be overridden "
            "with `--reload-include`. This option has no effect unless watchfiles is "
            "installed.",
            dest="reload_excludes",
        )
        parser.add_argument(
            "--reload-delay",
            type=float,
            default=0.25,
            help="Delay between previous and next check if application needs to be."
            " Defaults to 0.25s.",
        )
        parser.add_argument(
            "--workers",
            type=int,
            help="Number of worker processes. Defaults to the $WEB_CONCURRENCY environment"
            " variable if available, or 1. Not valid with --reload.",
        )
        parser.add_argument(
            "--loop",
            type=LOOP_CHOICES,
            default="auto",
            help="Event loop implementation.",
        )
        parser.add_argument(
            "--http",
            type=HTTP_CHOICES,
            default="auto",
            help="HTTP protocol implementation.",
        )
        parser.add_argument(
            "--ws",
            type=WS_CHOICES,
            default="auto",
            help="WebSocket protocol implementation.",
        )
        parser.add_argument(
            "--ws-max-size",
            type=int,
            default=16777216,
            help="WebSocket max size message in bytes",
        )
        parser.add_argument(
            "--ws-ping-interval",
            type=float,
            default=20.0,
            help="WebSocket ping interval",
        )
        parser.add_argument(
            "--ws-ping-timeout",
            type=float,
            default=20.0,
            help="WebSocket ping timeout",
        )
        parser.add_argument(
            "--ws-per-message-deflate",
            type=bool,
            default=True,
            help="WebSocket per-message-deflate compression",
        )
        parser.add_argument(
            "--lifespan",
            type=LIFESPAN_CHOICES,
            default="auto",
            help="Lifespan implementation.",
        )
        parser.add_argument(
            "--interface",
            type=INTERFACE_CHOICES,
            default="auto",
            help="Select ASGI3, ASGI2, or WSGI as the application interface.",
        )
        parser.add_argument(
            "--env-file",
            type=click.Path(exists=True),
            help="Environment configuration file.",
        )
        parser.add_argument(
            "--log-config",
            type=click.Path(exists=True),
            help="Logging configuration file. Supported formats: .ini, .json, .yaml.",
        )
        parser.add_argument(
            "--log-level",
            type=LEVEL_CHOICES,
            help="Log level. [default: info]",
        )
        parser.add_argument(
            "--no-access-log",
            action="store_false",
            help="Disable access log.",
            dest="access_log",
        )
        parser.add_argument(
            "--no-use-colors",
            action="store_false",
            help="Disable colorized logging.",
            dest="use_colors",
        )
        parser.add_argument(
            "--no-proxy-headers",
            action="store_false",
            help="Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to "
            "populate remote address info.",
            dest="proxy-headers",
        )
        parser.add_argument(
            "--no-server-header",
            action="store_false",
            help="Disable default Server header.",
            dest="server-header",
        )
        parser.add_argument(
            "--no-date-header",
            action="store_false",
            help="Disable default Date header.",
            dest="date-header",
        )
        parser.add_argument(
            "--root-path",
            default="",
            help="Set the ASGI 'root_path' for applications submounted below a given URL path.",
        )
        parser.add_argument(
            "--limit-concurrency",
            type=int,
            help="Maximum number of concurrent connections or tasks to allow, before issuing"
            " HTTP 503 responses.",
        )
        parser.add_argument(
            "--backlog",
            type=int,
            default=2048,
            help="Maximum number of connections to hold in backlog",
        )
        parser.add_argument(
            "--limit-max-requests",
            type=int,
            help="Maximum number of requests to service before terminating the process.",
        )
        parser.add_argument(
            "--timeout-keep-alive",
            type=int,
            default=5,
            help="Close Keep-Alive connections if no new data is received within this timeout.",
        )
        parser.add_argument(
            "--ssl-keyfile",
            help="SSL key file",
        )
        parser.add_argument(
            "--ssl-certfile",
            help="SSL certificate file",
        )
        parser.add_argument(
            "--ssl-keyfile-password",
            help="SSL keyfile password",
        )
        parser.add_argument(
            "--ssl-version",
            type=int,
            default=int(SSL_PROTOCOL_VERSION),
            help="SSL version to use (see stdlib ssl module's)",
        )
        parser.add_argument(
            "--ssl-cert-reqs",
            type=int,
            default=int(ssl.CERT_NONE),
            help="Whether client certificate is required (see stdlib ssl module's)",
        )
        parser.add_argument(
            "--ssl-ca-certs",
            help="CA certificates file",
        )
        parser.add_argument(
            "--ssl-ciphers",
            default="TLSv1",
            help="Ciphers to use (see stdlib ssl module's)",
        )
        parser.add_argument(
            "--header",
            nargs="*",
            help="Specify custom default HTTP response headers as a Name:Value pair",
            dest="headers",
        )
        parser.add_argument(
            "--app-dir",
            default=".",
            help="Look for APP in the specified directory, by adding this to the PYTHONPATH."
            " Defaults to the current working directory.",
        )
        parser.add_argument(
            "--h11-max-incomplete-event-size",
            type=int,
            default=DEFAULT_MAX_INCOMPLETE_EVENT_SIZE,
            help="For h11, the maximum number of bytes to buffer of an incomplete event.",
            dest="h11_max_incomplete_event_size",
        )
        parser.add_argument(
            "--factory",
            action="store_true",
            help="Treat APP as an application factory, i.e. a () -> <ASGI app> callable.",
        )

    def handle(self, *args, **options):
        options.setdefault("debug", self.DEBUG)
        options.setdefault("forwarded_allow_ips", self.ALLOWED_IPS)

        uvicorn_options = self.parse_uvicorn_options(**options)
        uvicorn.run(server_path, **uvicorn_options)

    @staticmethod
    def parse_uvicorn_options(**options) -> dict[str, any]:
        signature = inspect.signature(uvicorn.Config)
        keys = tuple(
            parameter.name
            for parameter in signature.parameters.values()
            if parameter.kind == parameter.POSITIONAL_OR_KEYWORD
        )
        return {key: value for key in keys if (value := options.get(key)) is not None}
