from blacksheep.server.controllers import ApiController

from sources.application.handlers import PollHandler


class PollsController(ApiController):
    poll_handler: PollHandler

    def __init__(self):
        self.poll_handler = PollHandler.get_instance()

    @classmethod
    def class_name(cls) -> str:
        return "polls"
