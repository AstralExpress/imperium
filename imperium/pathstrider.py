import pluggy

hookspec = pluggy.HookspecMarker("pathstrider")
PATHSTRIDER_MARKER = "pathstrider"


class Pathstrider:
    @hookspec
    def hello(self, message: str):
        """Initialize plugin (prepare configs, volumes, etc.)."""
