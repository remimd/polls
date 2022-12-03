from dataclasses import dataclass

from typing_extensions import Self


@dataclass(frozen=True)
class Tag:
    value: str

    @classmethod
    def create(cls, *args, **kwargs) -> Self:
        return cls(*args, **kwargs)
