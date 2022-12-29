from common.infrastructure.server import Server
from sources.infrastructure.uvicorn.server import UvicornServer


def create_server() -> Server:
    return UvicornServer()
