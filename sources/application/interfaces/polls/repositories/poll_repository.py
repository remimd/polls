from abc import abstractmethod

from common.repository import Repository
from sources.domains.polls.entities import Poll


class IPollRepository(Repository):
    @abstractmethod
    def add(self, poll: Poll):
        raise NotImplementedError
