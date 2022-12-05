from abc import ABC, abstractmethod

from common.repository import Repository
from sources.domains.polls.entities import Poll


class IPollRepository(Repository, ABC):
    @abstractmethod
    def add(self, poll: Poll):
        raise NotImplementedError
