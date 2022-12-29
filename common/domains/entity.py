from abc import ABCMeta
from typing import Any, Optional
from uuid import UUID, uuid4


class _EntityMeta(ABCMeta):
    def __call__(cls, *args, id: UUID | str = None, **kwargs):  # noqa
        instance = super().__call__(*args, **kwargs)
        instance._id = cls._get_uuid(id)
        return instance

    @staticmethod
    def _get_uuid(uuid: Optional[UUID | str]) -> UUID:
        if isinstance(uuid, UUID):
            return uuid

        if not uuid:
            return uuid4()

        return UUID(uuid)


class Entity(metaclass=_EntityMeta):
    _id: UUID

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name} {self.id}"

    def __eq__(self, other: Any) -> bool:
        is_same_class = self.__class__ == other.__class__
        return is_same_class and self.id == other.id

    @property
    def id(self) -> UUID:
        return self._id
