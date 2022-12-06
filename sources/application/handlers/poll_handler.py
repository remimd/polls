from typing import Type

from sources.application.protocols.polls.repositories import PPollRepository
from sources.domains.polls.entities import Poll


class PollHandler:
    def __init__(self, poll_repository: Type[PPollRepository]):
        self.poll_repository = poll_repository()

    async def create(self, question: str) -> Poll:
        poll = Poll.create(question)
        await self.poll_repository.add(poll)
        return poll
