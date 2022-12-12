from blacksheep import FromJSON, Response, pretty_json
from blacksheep.server.controllers import ApiController, get, post

from sources.application.handlers import PollHandler
from sources.infrastructure.adapters.polls.repositories import PollRepository
from sources.infrastructure.api.serializers import PollSerializer
from sources.infrastructure.api.validation import PollCreation


class PollsController(ApiController):
    def __init__(self):
        self.poll_handler = PollHandler(
            PollRepository(),
        )

    @classmethod
    def class_name(cls) -> str:
        return "polls"

    @post("create")
    async def create_poll(self, payload: FromJSON[PollCreation]) -> Response:
        kwargs = payload.value.dict()
        poll = await self.poll_handler.create(**kwargs)
        data = PollSerializer.transform(poll)
        return pretty_json(status=201, data=data)

    @get(":id")
    async def get_poll(self, id: str) -> Response:  # noqa
        poll = await self.poll_handler.get(id)
        data = PollSerializer.transform(poll)
        return pretty_json(data=data)
