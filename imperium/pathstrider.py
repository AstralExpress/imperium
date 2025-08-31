from abc import abstractmethod, ABC

import pluggy

hookspec = pluggy.HookspecMarker("pathstrider")
PATHSTRIDER_MARKER = "pathstrider"


class Pathstrider:
    @hookspec
    def init_plugin(self, logger, config, base_dir):
        """Initialize plugin (prepare configs, volumes, etc.)."""

    @hookspec
    def start_plugin(self):
        """Start plugin containers, attach them to the given network."""

    @hookspec
    def stop_plugin(self):
        """Stop plugin containers and clean up resources."""


class BasePathstrider(ABC):
    """Abstract implementation for pathstrider plugin."""

    @abstractmethod
    def init_plugin(self, logger, config, base_dir):
        """Initialize plugin (prepare configs, volumes, etc.)."""
        ...

    @abstractmethod
    def start_plugin(self):
        """Start plugin containers, attach them to the given network."""

    @abstractmethod
    def stop_plugin(self):
        """Stop plugin containers and clean up resources."""
