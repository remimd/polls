from abc import ABC
from typing import Any

from pydantic import BaseModel


class Serializer(BaseModel, ABC):
    class Config:
        orm_mode = True

    @classmethod
    def transform(cls, obj: Any) -> Any:
        return cls.from_orm(obj)
