from uuid import UUID

from common.serializer import Serializer


class TagSerializer(Serializer):
    value: str

    def dict(self, *args, **kwargs):
        return self.value


class AnswerSerializer(Serializer):
    id: UUID
    value: str


class PollSerializer(Serializer):
    id: UUID
    question: str
    answers: tuple[AnswerSerializer]
    tags: tuple[TagSerializer]
