from typing import Protocol

from sources.domains.polls.entities import Poll


class PPollRepository(Protocol):
    async def add(self, poll: Poll):
        ...

    async def get(self, poll_id: str) -> Poll:
        ...

    async def remove(self, poll_id: str):
        ...
