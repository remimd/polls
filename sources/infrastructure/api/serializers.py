from uuid import UUID

from .basis import Serializer


class TagSerializer(Serializer):
    value: str

    def dict(self, *args, **kwargs) -> str:
        return self.value


class AnswerSerializer(Serializer):
    id: UUID
    value: str


class PollSerializer(Serializer):
    id: UUID
    question: str
    answers: tuple[AnswerSerializer, ...]
    tags: tuple[TagSerializer, ...]
