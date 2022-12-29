from abc import ABC
from typing import Any


class ApiError(Exception, ABC):
    def __init__(self, status_code: int = 400, content: Any = None):
        self.status_code = status_code
        self.content = content


class UnprocessableError(ApiError):
    def __init__(self, errors: dict[str, str]):
        super().__init__(status_code=422, content=errors)


class InvalidCredentialsError(ApiError):
    def __init__(self, content: Any = None):
        super().__init__(status_code=401, content=content)
