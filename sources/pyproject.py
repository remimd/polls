from dataclasses import dataclass, fields
from pathlib import Path
from typing import Iterator, final

import toml


@final
@dataclass(frozen=True, slots=True)
class _PyProject:
    name: str
    version: str

    @classmethod
    def read(cls):
        path = Path(__file__).resolve().parent.parent / "pyproject.toml"

        with open(path) as file:
            data = toml.load(file)

        info = data["tool"]["poetry"]
        kwargs = {name: info.get(name) for name in cls.fields_name()}
        return _PyProject(**kwargs)

    @classmethod
    def fields_name(cls) -> Iterator[str]:
        for field in fields(cls):
            yield field.name


pyproject = _PyProject.read()
