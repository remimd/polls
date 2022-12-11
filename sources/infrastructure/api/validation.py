from .basis import Validator


class PollCreation(Validator):
    question: str
    answers: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
