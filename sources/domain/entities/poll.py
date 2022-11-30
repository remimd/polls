from dataclasses import field

from common.annotations import entity
from sources.domain.entities.answer import Answer


@entity
class Poll:
    question: str
    answers: list[Answer] = field(default_factory=list)
