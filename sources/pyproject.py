from dataclasses import dataclass, fields
from typing import final

import toml
from typing_extensions import Self


@final
@dataclass(frozen=True, slots=True)
class _PyProject:
    name: str
    version: str
    description: str

    @classmethod
    def read(cls) -> Self:
        with open("pyproject.toml") as file:
            data = toml.load(file)["tool"]["poetry"]

        kwargs = {
            field.name: data.get(field.name)
            for field in fields(cls)
        }
        return _PyProject(**kwargs)

    @property
    def name_snake_case(self) -> str:
        return (
            self.name.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "_")
        )


pyproject = _PyProject.read()
