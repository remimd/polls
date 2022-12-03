from dataclasses import dataclass

from typing_extensions import Self

from common.domain import Entity


@dataclass(eq=False)
class Answer(Entity):
    value: str

    @classmethod
    def create(cls, *args, **kwargs) -> Self:
        return cls(*args, **kwargs)
