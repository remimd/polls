import inspect
from abc import ABCMeta
from threading import Lock


_lock = Lock()


class Injectable(ABCMeta):
    _injectables = dict()

    def __new__(mcs, name, parents, *args, **kwargs):
        cls = super().__new__(mcs, name, parents, *args, **kwargs)

        with _lock:
            if inspect.isabstract(cls):
                mcs._set(cls)
            else:
                mcs._populate(cls, parents)

        return cls

    def __repr__(cls) -> str:
        return f"<{cls.__name__}>"

    @classmethod
    def _set(mcs, reference, injectable=None):
        mcs._injectables[reference] = injectable

    @classmethod
    def _populate(mcs, cls, parents):
        for reference, injectable in mcs._injectables.items():
            if reference not in parents:
                continue

            if injectable:
                raise RuntimeError(
                    f"Multiple implementations for {reference.__name__}."
                )

            mcs._set(reference, cls())
            break


def get_injectable(reference):
    return Injectable._injectables.get(reference)


def is_injectable(reference) -> bool:
    return issubclass(type(reference), Injectable)


class Injected(ABCMeta):
    def __call__(cls, *args, **kwargs):
        signature = inspect.signature(cls.__init__)
        parameters = signature.parameters

        for name, parameter in parameters.items():
            annotation = parameter.annotation
            if not is_injectable(annotation) and not kwargs.get(name):
                continue

            if injectable := get_injectable(annotation):
                kwargs[name] = injectable
                break

            raise RuntimeError(f"{annotation.__name__} implementation doesn't exist.")

        return super().__call__(*args, **kwargs)
