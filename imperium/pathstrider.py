import pluggy

hookspec = pluggy.HookspecMarker("pathstrider")
PATHSTRIDER_MARKER = "pathstrider"


class Pathstrider:
    @hookspec
    def init_plugin(self, logger):
        """Initialize plugin (prepare configs, volumes, etc.)."""

    @hookspec
    def start_plugin(self):
        """Start plugin containers, attach them to the given network."""

    @hookspec
    def stop_plugin(self):
        """Stop plugin containers and clean up resources."""
