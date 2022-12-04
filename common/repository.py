from __future__ import annotations

from abc import ABCMeta
from threading import Lock
from typing import Optional, Type


_lock = Lock()


class _RepositoryMeta(ABCMeta):
    _base: RepositoryType = None
    _repositories: dict[RepositoryType, Optional[Repository]] = {}

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)

        if not mcs._base:
            mcs._base = cls
        elif issubclass(cls, mcs._base):
            mcs._populate(cls)
        else:
            raise RuntimeError(
                f"Please inherit from {mcs._base.__name__}, "
                f"don't use metaclass={mcs.__name__}."
            )

        return cls

    def __repr__(cls) -> str:
        return f"<{cls.__name__}>"

    @classmethod
    def get_repository(mcs, interface: RepositoryType) -> Optional[Repository]:
        return mcs._repositories.get(interface)

    @classmethod
    def _set(mcs, interface: RepositoryType, repository: Repository = None):
        mcs._repositories[interface] = repository
        return mcs

    @classmethod
    def _populate(mcs, cls: RepositoryType):
        is_implementation = False

        with _lock:
            for interface, repository in mcs._repositories.items():
                if not issubclass(cls, interface):
                    continue

                if repository:
                    raise RuntimeError(
                        f"Multiple implementations for {interface.__name__}."
                    )

                is_implementation = True
                mcs._set(interface, cls())
                break

            if not is_implementation:
                mcs._set(cls)


class Repository(metaclass=_RepositoryMeta):
    pass


RepositoryType = Type[Repository]
