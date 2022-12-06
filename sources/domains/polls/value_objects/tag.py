from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    value: str

    @classmethod
    def create(cls, value: str, *args, **kwargs):
        value = value.lower()
        return cls(value, *args, **kwargs)
