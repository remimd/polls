from blacksheep import Application

from common.infrastructure.server import Server
from sources.infrastructure import configuration
from sources.infrastructure.api import APIComponent
from sources.infrastructure.command import CommandManager
from sources.infrastructure.django import DjangoComponent
from sources.infrastructure.uvicorn import UvicornServer


application = Application(show_error_details=configuration.debug)


def create_server() -> Server:
    app = f"{__name__}:application"
    manager = CommandManager()
    components = DjangoComponent(), APIComponent()

    return UvicornServer(app, manager, components)
