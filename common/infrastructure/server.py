import sys
from abc import ABC, abstractmethod
from typing import Any, Iterable, Protocol


class CommandManager(Protocol):
    def execute(self, *args, **kwargs):
        ...


class Component(Protocol):
    def setup(self):
        ...


class Server(ABC):
    def __init__(
        self,
        application: Any,
        manager: CommandManager = None,
        components: Iterable[Component] = (),
    ):
        self.application = application
        self.manager = manager
        self.components = components
        self._setup()

    def run(self, **kwargs):
        argv = sys.argv

        if self.manager:
            self.manager.execute(*argv, **kwargs)
        else:
            self.start(*argv, **kwargs)

    @abstractmethod
    def start(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def _setup(self):
        for component in self.components:
            component.setup()
