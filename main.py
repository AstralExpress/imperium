import pluggy

hookspec = pluggy.HookspecMarker("orchestrator")

class Pathstrider:
    @hookspec
    def hello(self, message: str):
        """Initialize plugin (prepare configs, volumes, etc.)."""

