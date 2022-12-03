from common.handler import Handler
from sources.application.interfaces.polls.repositories import IPollRepository
from sources.domains.polls.entities import Poll


class PollHandler(Handler):
    poll_repository: IPollRepository

    def __init__(self, poll_repository: IPollRepository):
        self.poll_repository = poll_repository

    def create(self, question: str) -> Poll:
        poll = Poll.create(question)
        self.poll_repository.add(poll)
        return poll
