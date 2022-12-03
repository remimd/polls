from blacksheep.server.controllers import ApiController


class PollsController(ApiController):
    @classmethod
    def class_name(cls) -> str:
        return "polls"
