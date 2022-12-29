from abc import ABC

from pydantic import BaseModel, ValidationError

from sources.infrastructure.exceptions import UnprocessableError


class Validator(BaseModel, ABC):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except ValidationError as exc:
            errors = {error._loc: error.exc.msg_template for error in exc.raw_errors}
            raise UnprocessableError(errors) from exc
