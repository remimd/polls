from typing import Protocol

from sources.domains.polls.entities import Poll


class PPollRepository(Protocol):
    async def add(self, poll: Poll):
        ...
