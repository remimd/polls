from blacksheep import FromJSON, pretty_json
from blacksheep.server.controllers import ApiController, post

from sources.application.handlers import PollHandler
from sources.infrastructure.adapters.polls.repositories import PollRepository
from sources.infrastructure.api.validation import PollCreation


class PollsController(ApiController):
    def __init__(self):
        self.poll_handler = PollHandler(PollRepository)

    @classmethod
    def class_name(cls) -> str:
        return "polls"

    @post("create")
    async def create(self, payload: FromJSON[PollCreation]):
        kwargs = payload.value.dict()
        poll = await self.poll_handler.create(**kwargs)
        return pretty_json(status=201, data=poll)
