from blacksheep import created
from blacksheep.server.controllers import ApiController, post

from sources.application.handlers import PollHandler


class PollsController(ApiController):
    poll_handler: PollHandler

    def __init__(self):
        self.poll_handler = PollHandler.get_instance()

    @classmethod
    def class_name(cls) -> str:
        return "polls"

    @post("create")
    def create(self):
        return created()
