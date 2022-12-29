from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from django.db import transaction

from sources.domains.access.entities import User
from sources.infrastructure.adapters.mixins.repositories import DjangoRepositoryMixin
from sources.infrastructure.django.core.models import UserORM


class UserRepository(DjangoRepositoryMixin):
    async def register(self, user: User, password: str):
        await sync_to_async(self._register)(user, password)

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
