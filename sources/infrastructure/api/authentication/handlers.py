from typing import Optional

from blacksheep import Request
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity

from sources.infrastructure.handlers import access_handler
from sources.infrastructure.utils.jwt import InvalidToken, validate_access


class JWTHandler(AuthenticationHandler):
    MODE = "JWT"

    def __init__(self):
        super().__init__()
        self.handler = access_handler

    async def authenticate(self, context: Request) -> Optional[Identity]:
        authorization_value = context.get_first_header(b"Authorization")

        if not authorization_value or not authorization_value.startswith(b"Bearer "):
            return None

        token = authorization_value[7:].decode()

        try:
            token = validate_access(token)
        except InvalidToken:
            return None

        pk = token.get("pk")
        user = await self.handler.get_user(pk, no_exception=True)

        if not user:
            return None

        context.identity = Identity({"user": user}, self.MODE)
        return context.identity
