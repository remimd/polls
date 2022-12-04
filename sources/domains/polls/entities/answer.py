from dataclasses import dataclass, field

from common.domain import Entity


@dataclass(eq=False)
class Answer(Entity):
    value: str

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
