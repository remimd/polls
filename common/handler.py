import inspect
from abc import ABCMeta

from common.patterns import Singleton
from common.repository import Repository


class _HandlerMeta(ABCMeta):
    def __call__(cls, *args, **kwargs):
        signature = inspect.signature(cls.__init__)
        parameters = signature.parameters

        for name, parameter in parameters.items():
            annotation = parameter.annotation
            if not issubclass(annotation, Repository):
                continue

            if repository := Repository.get_repository(annotation):
                kwargs[name] = repository
                break

            raise RuntimeError(f"{annotation.__name__} implementation doesn't exist.")

        return super().__call__(*args, **kwargs)


class Handler(Singleton, metaclass=_HandlerMeta):
    pass
