from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional, final

import jwt

from sources.infrastructure import configuration


class InvalidToken(Exception):
    ...


class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1


@final
@dataclass(frozen=True, slots=True)
class Token:
    data: dict[str, Any]
    type: TokenType = field(default=None)
    expiration: datetime = field(default=None)

    # Static fields
    _KEY = configuration.secret_key

    def __str__(self) -> str:
        name = "Token"

        if _type := self.type:
            name = f"{_type.name.title()} {name}"

        return name

    @classmethod
    def decode(cls, encoded: str) -> Token:
        try:
            decoded = jwt.decode(encoded, cls._KEY, algorithms=("HS256",))
        except jwt.InvalidTokenError as exc:
            raise InvalidToken(str(exc)) from exc

        return cls._from_dict(decoded)

    @classmethod
    def _from_dict(cls, data: dict[str, Any]) -> Token:
        kwargs = {}

        if (token_type := data.pop("type", None)) is not None:
            kwargs["type"] = TokenType(token_type)

        if expiration := data.pop("exp", None):
            kwargs["expiration"] = datetime.utcfromtimestamp(expiration)

        return cls(data, **kwargs)

    @property
    def is_access_token(self) -> bool:
        return self.type == TokenType.ACCESS

    @property
    def is_refresh_token(self) -> bool:
        return self.type == TokenType.REFRESH

    def encode(self) -> str:
        return jwt.encode(self._to_dict(), self._KEY, algorithm="HS256")

    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key)

    def _to_dict(self) -> dict[str, Any]:
        data = {}

        if token_type := self.type:
            data["type"] = token_type.value

        if expiration := self.expiration:
            data["exp"] = expiration

        return self.data | data


@final
@dataclass(frozen=True, slots=True)
class AuthenticationTokens:
    access: Token
    refresh: Token

    def encode(self) -> dict[str, str]:
        return {
            "access": self.access.encode(),
            "refresh": self.refresh.encode(),
        }


def validate_access(encoded: str) -> Token:
    token = Token.decode(encoded)

    if not token.is_access_token:
        raise InvalidToken("Token isn't a valid access token.")

    return token


def validate_refresh(encoded: str, data: dict[str, Any] = None) -> Token:
    token = Token.decode(encoded)
    has_expected_data = not data or data == token.data

    if not token.is_refresh_token and not has_expected_data:
        raise InvalidToken("Token isn't a valid refresh token.")

    return token


def generate_authentication_tokens(
    data: dict[str, Any],
    access_lifespan: timedelta = timedelta(minutes=30),
    refresh_lifespan: timedelta = timedelta(days=200),
) -> AuthenticationTokens:
    now = datetime.now(tz=timezone.utc)

    access = Token(data, type=TokenType.ACCESS, expiration=now + access_lifespan)
    refresh = Token(data, type=TokenType.REFRESH, expiration=now + refresh_lifespan)

    return AuthenticationTokens(access, refresh)
