from typing import Any, Protocol


class PAuthentication(Protocol):
    async def login(self, username: str, password: str) -> Any:
        ...

    async def refresh(self, *args, **kwargs) -> Any:
        ...
