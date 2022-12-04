from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    value: str

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
