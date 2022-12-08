from typing import Type, Iterable

from sources.application.protocols.polls.repositories import PPollRepository
from sources.domains.polls.entities import Poll


class PollHandler:
    def __init__(self, poll_repository: PPollRepository):
        self.poll_repository = poll_repository

    async def create(
        self,
        question: str,
        answers: Iterable[str] = tuple(),
        tags: Iterable[str] = tuple(),
    ) -> Poll:
        poll = Poll.create(question)

        for answer in answers:
            poll.add_answer(answer)

        for tag in tags:
            poll.add_tag(tag)

        await self.poll_repository.add(poll)
        return poll
