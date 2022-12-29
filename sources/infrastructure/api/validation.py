from .basis import Validator


class Credentials(Validator):
    username: str
    password: str


class UserRegistration(Validator):
    email: str
    password: str
    first_name: str = None
    last_name: str = None
    phone: str = None


class PollCreation(Validator):
    question: str
    answers: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
