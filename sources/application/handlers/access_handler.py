from typing import Any, Optional

from sources.application.protocols.access import PAuthentication
from sources.application.protocols.access.repositories import PUserRepository
from sources.domains.access.entities import User


class AccessHandler:
    def __init__(
        self,
        authentication: PAuthentication,
        user_repository: PUserRepository,
    ):
        self.authentication = authentication
        self.user_repository = user_repository

    async def register(self, *args, password: str, **kwargs) -> User:
        user = User.create(*args, **kwargs)
        await self.user_repository.register(user, password)
        return user

    async def login(self, username: str, password: str) -> Any:
        return await self.authentication.login(username, password)

    async def refresh(self, *args, **kwargs) -> Any:
        return await self.authentication.refresh(*args, **kwargs)

    async def get_user(
        self,
        user_id: str,
        no_exception: bool = False,
    ) -> User | Optional[User]:
        return await self.user_repository.get(user_id, no_exception)
