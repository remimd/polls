from typing import Any

from asgiref.sync import sync_to_async
from django.contrib.auth.backends import UserModel

from sources.infrastructure.exceptions import InvalidCredentialsError
from sources.infrastructure.utils.jwt import (
    generate_authentication_tokens,
    validate_refresh,
)


class Authentication:
    USERNAME_FIELD = UserModel.USERNAME_FIELD

    async def login(self, username: str, password: str) -> dict[str, str]:
        return await sync_to_async(self._login)(username, password)

    async def refresh(self, refresh_token: str, pk: Any) -> dict[str, str]:
        return await sync_to_async(self._refresh)(refresh_token, pk)

    def _login(self, username: str, password: str) -> dict[str, str]:
        options = {self.USERNAME_FIELD: username}

        try:
            user = UserModel.objects.get(**options)
        except UserModel.DoesNotExist as exc:
            raise InvalidCredentialsError from exc

        if not user.check_password(password):
            raise InvalidCredentialsError

        data = {"pk": user.pk}
        authentication_tokens = generate_authentication_tokens(data)
        return authentication_tokens.encode()

    def _refresh(self, refresh_token: str, pk: Any) -> dict[str, str]:
        validate_refresh(refresh_token, {"pk": pk})
