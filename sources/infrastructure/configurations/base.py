from abc import ABC
from os import getenv

from tzlocal import get_localzone_name

from common.infrastructure.configuration import Configuration, MISSING
from sources.pyproject import pyproject


class BaseConfiguration(Configuration, ABC):
    allowed_hosts = ("127.0.0.1", "localhost")
    debug = False
    db_name = getenv("DB_NAME", MISSING)
    db_user = getenv("DB_USER", "root")
    db_password = getenv("DB_PASSWORD", "root")
    db_host = getenv("DB_HOST", "localhost")
    db_port = getenv("DB_PORT", 5432)
    name = pyproject.name.title()
    secret_key = getenv("SECRET_KEY", MISSING)
    swagger_endpoint = "/"
    time_zone = get_localzone_name()
    version = pyproject.version
