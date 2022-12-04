from abc import ABC
from threading import Lock


_lock = Lock()


class Singleton(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        with _lock:
            if cls._instance:
                raise RuntimeError(f"{cls.__name__} can only be built once.")
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls()

        return cls._instance


class StaticClass(ABC):
    def __new__(cls, *args, **kwargs):
        raise RuntimeError(f"{cls.__name__} can't be instantiated.")
