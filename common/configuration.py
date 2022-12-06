from abc import ABC
from enum import Enum, auto

from pydantic import BaseModel


class _States(Enum):
    MISSING = auto()

    def __str__(self) -> str:
        return self.name


MISSING = _States.MISSING


class Configuration(BaseModel, ABC):
    @classmethod
    def verify(cls):
        instance = cls()

        for key, value in vars(instance).items():
            match value:
                case _States.MISSING:
                    raise ValueError(f'"{key}" missing in the configuration.')

        return instance
