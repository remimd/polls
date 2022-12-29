from blacksheep import FromJSON, Response, no_content, pretty_json
from blacksheep.server.controllers import ApiController, delete, get, post

from sources.infrastructure.api.serializers import PollSerializer
from sources.infrastructure.api.validation import PollCreation
from sources.infrastructure.handlers import poll_handler


class PollsController(ApiController):
    def __init__(self):
        self.handler = poll_handler

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
