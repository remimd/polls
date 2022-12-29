from blacksheep import FromJSON, Response, allow_anonymous, pretty_json
from blacksheep.server.controllers import ApiController, post

from sources.infrastructure.api.serializers import UserSerializer
from sources.infrastructure.api.validation import Credentials, UserRegistration
from sources.infrastructure.handlers import access_handler


class AccessController(ApiController):
    def __init__(self):
        self.handler = access_handler

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
