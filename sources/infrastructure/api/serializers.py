from typing import Optional
from uuid import UUID

from phonenumbers import PhoneNumber, PhoneNumberFormat, format_number
from pydantic import validator

from .basis import Serializer


class UserSerializer(Serializer):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    phone: Optional[str]

    @validator("phone", pre=True)
    def phone_validator(cls, value):
        if isinstance(value, PhoneNumber):
            value = format_number(value, PhoneNumberFormat.INTERNATIONAL)

        return value


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
