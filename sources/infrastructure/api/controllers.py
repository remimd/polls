from blacksheep import created
from blacksheep.server.controllers import ApiController, post

from sources.application.handlers import PollHandler


class PollsController(ApiController):
    def __init__(self):
        self.poll_handler = PollHandler()

    @classmethod
    def class_name(cls) -> str:
        return "polls"

    @post("create")
    async def create(self):
        self.poll_handler.create("")
        return created()
