from dataclasses import dataclass, field

from common.domain import Entity
from sources.domains.polls.entities import Answer
from sources.domains.polls.value_objects import Tag


@dataclass(eq=False)
class Poll(Entity):
    question: str
    answers: list[Answer] = field(default_factory=list)
    tags: set[Tag] = field(default_factory=set)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def add_answer(self, answer: Answer):
        self.answers.append(answer)
        return self

    def add_tag(self, tag: Tag):
        self.tags.add(tag)
        return self

    def remove_tag(self, tag: Tag):
        self.tags.remove(tag)
        return self
