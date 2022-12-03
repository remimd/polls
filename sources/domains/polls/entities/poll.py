from dataclasses import dataclass, field

from typing_extensions import Self

from common.domain import Entity
from sources.domains.polls.entities import Answer
from sources.domains.polls.value_objects import Tag


@dataclass(eq=False)
class Poll(Entity):
    question: str
    answers: list[Answer] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)

    @classmethod
    def create(cls, *args, **kwargs) -> Self:
        return cls(*args, **kwargs)

    def add_answer(self, answer: Answer) -> Self:
        self.answers.append(answer)
        return self

    def add_tag(self, tag: Tag) -> Self:
        self.tags.append(tag)
        return self

    def remove_tag(self, tag: Tag) -> Self:
        self.tags.remove(tag)
        return self
