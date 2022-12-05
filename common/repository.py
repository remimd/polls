from abc import ABC

from common.interface import Interface


class Repository(Interface, ABC):
    def __repr__(self) -> str:
        return f"<repository {self.__class__.__name__}>"
