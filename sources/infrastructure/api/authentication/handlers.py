from typing import Any, Optional

from asgiref.sync import sync_to_async
from blacksheep import Request
from django.contrib.auth.backends import UserModel
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity

from sources.domains.access.entities import User
from sources.infrastructure.utils.jwt import InvalidToken, validate_access


class DjangoJWTHandler(AuthenticationHandler):
    MODE = "DjangoJWT"

    async def authenticate(self, context: Request) -> Optional[Identity]:
        authorization_value = context.get_first_header(b"Authorization")

        if not authorization_value or not authorization_value.startswith(b"Bearer "):
            return None

        token = authorization_value[7:].decode()

        try:
            token = validate_access(token)
        except InvalidToken:
            return None

        user_pk = token.get("pk")
        user_orm = await self.get_user(user_pk)

        if not user_orm:
            return None

        kwargs = {
            "id": user_orm.id,
            "email": user_orm.email,
            "first_name": user_orm.first_name,
            "last_name": user_orm.last_name,
            "phone": user_orm.phone,
        }
        user = User(**kwargs)

        context.identity = Identity({"user": user}, self.MODE)
        return context.identity

    @classmethod
    async def get_user(cls, user_pk: Any) -> Optional[UserModel]:
        return await sync_to_async(cls._get_user)(user_pk)

    @staticmethod
    def _get_user(user_pk: Any) -> Optional[UserModel]:
        if user_pk in (None, ""):
            return None

        try:
            return UserModel.objects.get(pk=user_pk)
        except UserModel.DoesNotExist:
            return None
