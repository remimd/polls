from abc import ABCMeta

from common.patterns import Singleton


class _HandlerMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class Handler(Singleton, metaclass=_HandlerMeta):
    pass
