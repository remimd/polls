from typing import Optional

from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from django.db import transaction

from sources.domains.access.entities import User
from sources.infrastructure.adapters.mixins.repositories import DjangoRepositoryMixin
from sources.infrastructure.orm.models import UserORM


class UserRepository(DjangoRepositoryMixin):
    async def register(self, user: User, password: str):
        await sync_to_async(self._register)(user, password)

    async def get(
        self,
        user_id: str,
        no_exception: bool = False,
    ) -> User | Optional[User]:
        return await sync_to_async(self._get)(user_id, no_exception)

    @transaction.atomic
    def _register(self, user: User, password: str):
        UserORM.objects.create(
            id=user.id,
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            password=make_password(password),
        )

    def _get(self, user_id: str, no_exception: bool) -> User | Optional[User]:
        try:
            user_orm = UserORM.objects.get(id=user_id)
        except BaseException as exc:
            if no_exception:
                return None
            else:
                raise exc

        return User.create(
            id=user_orm.id,
            email=user_orm.email,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            phone=user_orm.phone,
        )
