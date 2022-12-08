from common.validator import Validator


class PollCreation(Validator):
    question: str
    answers: tuple[str, ...]
    tags: tuple[str, ...]
