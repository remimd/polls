from typing import Protocol

from sources.domains.access.entities import User


class PUserRepository(Protocol):
    async def register(self, user: User, password: str):
        ...
