from __future__ import annotations

from abc import ABC
from os import getenv
from pathlib import Path
from typing import Type

from tzlocal import get_localzone_name

from common.patterns import StaticClass
from sources.pyproject import pyproject


class _Missing:
    pass


MISSING = _Missing()


class BaseConfiguration(StaticClass, ABC):
    allowed_hosts = "127.0.0.1", "localhost"
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    debug = False
    db_name = getenv("DB_NAME", pyproject.name_snake_case)
    db_user = getenv("DB_USER", "root")
    db_password = getenv("DB_PASSWORD", "root")
    db_host = getenv("DB_HOST", "localhost")
    db_port = getenv("DB_PORT", 5432)
    documentation_endpoint = "/"
    name = pyproject.name.title()
    secret_key = getenv("SECRET_KEY", MISSING)
    time_zone = get_localzone_name()
    version = pyproject.version

    @classmethod
    def validate(cls) -> Type[BaseConfiguration]:
        # TODO: Check that there is no `MISSING`.
        return cls
