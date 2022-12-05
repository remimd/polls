import inspect
from abc import ABCMeta
from threading import Lock
from typing import Any, Iterator, Callable, Optional, Type


_lock = Lock()
_injectables = dict()


def _set(reference: Type, injectable=None):
    _injectables[reference] = injectable


def _implements(cls: Type, parents: tuple[Type, ...]):
    for reference, injectable in _injectables.items():
        if reference not in parents:
            continue

        if injectable:
            raise RuntimeError(f"Multiple implementations for {reference.__name__}.")

        _set(reference, cls())
        break


def get_injectable(reference: Type) -> Optional:
    return _injectables.get(reference)


class Injectable(ABCMeta):
    def __new__(mcs, name: str, parents: tuple[Type, ...], *args, **kwargs):
        cls = super().__new__(mcs, name, parents, *args, **kwargs)

        with _lock:
            if inspect.isabstract(cls):
                _set(cls)
            else:
                _implements(cls, parents)

        return cls

    def __repr__(cls) -> str:
        return f"<{cls.__name__}>"


def is_injectable(cls: Type) -> bool:
    return issubclass(type(cls), Injectable)


def _inspect_params(function: Callable) -> Iterator[tuple[str, Type]]:
    signature = inspect.signature(function)
    parameters = signature.parameters

    for name, param in parameters.items():
        yield name, param.annotation


def _injectable_kwargs(function: Callable) -> dict[str, Any]:
    kwargs = {}

    for name, annotation in _inspect_params(function):
        if not is_injectable(annotation):
            continue

        if injectable := get_injectable(annotation):
            kwargs[name] = injectable
            break

        raise RuntimeError(f"{annotation.__name__} implementation doesn't exist.")

    return kwargs


class Injected(ABCMeta):
    def __call__(cls, *args, **kwargs):
        new_kwargs = _injectable_kwargs(cls.__init__) | kwargs
        call = super().__call__

        try:
            return call(*args, **new_kwargs)
        except TypeError:
            return call(*args, **kwargs)
