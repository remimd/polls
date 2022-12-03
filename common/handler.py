from abc import ABC

from common.patterns import Singleton


class Handler(Singleton, ABC):
    pass
