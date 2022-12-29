from typing import Optional, Protocol

from sources.domains.access.entities import User


class PUserRepository(Protocol):
    async def register(self, user: User, password: str):
        ...

    async def get(
        self,
        user_id: str,
        no_exception: bool = False,
    ) -> User | Optional[User]:
        ...
