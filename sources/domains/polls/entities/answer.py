from dataclasses import dataclass

from common.domains.entity import Entity


@dataclass(eq=False)
class Answer(Entity):
    value: str

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
