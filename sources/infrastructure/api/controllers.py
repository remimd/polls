from blacksheep import FromJSON, Response, allow_anonymous, no_content, pretty_json
from blacksheep.server.controllers import ApiController, delete, get, post

from sources.application.handlers import AccessHandler, PollHandler
from sources.infrastructure.adapters.access import Authentication
from sources.infrastructure.adapters.access.repositories import UserRepository
from sources.infrastructure.adapters.polls.repositories import PollRepository
from sources.infrastructure.api.serializers import PollSerializer, UserSerializer
from sources.infrastructure.api.validation import (
    Credentials,
    PollCreation,
    UserRegistration,
)


class AccessController(ApiController):
    def __init__(self):
        self.handler = AccessHandler(
            Authentication(),
            UserRepository(),
        )

    @classmethod
    def class_name(cls) -> str:
        return "access"

    @allow_anonymous()
    @post("login")
    async def login(self, payload: FromJSON[Credentials]) -> Response:
        kwargs = payload.value.dict()
        data = await self.handler.login(**kwargs)
        return pretty_json(data=data)

    @allow_anonymous()
    @post("register")
    async def register(self, payload: FromJSON[UserRegistration]) -> Response:
        kwargs = payload.value.dict()
        user = await self.handler.register(**kwargs)
        data = UserSerializer.transform(user)
        return pretty_json(status=201, data=data)

    @post("refresh")
    async def refresh(self, payload: FromJSON) -> Response:
        ...


class PollsController(ApiController):
    def __init__(self):
        self.handler = PollHandler(
            PollRepository(),
        )

    @classmethod
    def class_name(cls) -> str:
        return "polls"

    @post("create")
    async def create_poll(self, payload: FromJSON[PollCreation]) -> Response:
        kwargs = payload.value.dict()
        poll = await self.handler.create(**kwargs)
        data = PollSerializer.transform(poll)
        return pretty_json(status=201, data=data)

    @get(":id")
    async def get_poll(self, id: str) -> Response:  # noqa
        poll = await self.handler.get(id)
        data = PollSerializer.transform(poll)
        return pretty_json(data=data)

    @delete(":id")
    async def remove_poll(self, id: str) -> Response:  # noqa
        await self.handler.remove(id)
        return no_content()
