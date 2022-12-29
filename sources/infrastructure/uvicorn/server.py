import inspect

import uvicorn

from common.infrastructure.server import Server


class UvicornServer(Server):
    def start(self, **options):
        uvicorn_options = self._parse_options(**options)
        uvicorn.run(self.application, **uvicorn_options)

    @staticmethod
    def _parse_options(**options) -> dict[str, any]:
        signature = inspect.signature(uvicorn.Config)
        keys = tuple(
            parameter.name
            for parameter in signature.parameters.values()
            if parameter.kind == parameter.POSITIONAL_OR_KEYWORD
        )
        return {key: value for key in keys if (value := options.get(key)) is not None}
