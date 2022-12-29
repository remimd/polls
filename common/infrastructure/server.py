import sys
from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable


class CommandManager(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


class Component(ABC):
    def setup(self):
        ...


class Server(ABC):
    def __init__(
        self,
        application: Callable | str,
        manager: CommandManager = None,
        components: Iterable[Component] = (),
    ):
        self.application = application
        self.manager = manager
        self.components = components
        self._setup()

    def run(self):
        if self.manager:
            argv = sys.argv
            self.manager.execute(*argv)
        else:
            self.start()

    @abstractmethod
    def start(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def _setup(self):
        for component in self.components:
            component.setup()
