from sources.application.interfaces.polls.repositories import IPollRepository
from sources.domains.polls.entities import Poll


class PollRepository(IPollRepository):
    def add(self, poll: Poll):
        pass
