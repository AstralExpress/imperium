from pathlib import Path

from imperium.templates import DefaultPathstrider


# noinspection PyIncorrectDocstring
def pathstrider_factory(
        name: str,
        docker_compose_file: str | None = None,
        *,  # everything after must be passed as kwarg
        pre_init=None,
        post_init=None,
        pre_start=None,
        post_start=None,
        pre_stop=None,
        post_stop=None,
):
    """
    Factory for creating simple Pathstrider implementations.

    :param name: Name of the Pathstrider (used in logs).
    :param docker_compose_file: Optional path to a docker-compose.yml file.
                                Defaults to <base_dir>/docker-compose.yml.
    :param pre_init/post_init/pre_start/post_start/pre_stop/post_stop:
           Optional hook overrides as callables (self -> None).
    """

    class CustomPathstrider(DefaultPathstrider):
        def __init__(self):
            super().__init__()
            self.name = name
            if docker_compose_file:
                # Pre-resolve once if path is absolute, otherwise initialized to default in init_plugin
                self.docker_compose_file = str(Path(docker_compose_file))

        # --- Lifecycle Hooks ---
        def pre_init(self):
            if pre_init: pre_init(self)

        def post_init(self):
            if post_init: post_init(self)

        def pre_start(self):
            if pre_start: pre_start(self)

        def post_start(self):
            if post_start: post_start(self)

        def pre_stop(self):
            if pre_stop: pre_stop(self)

        def post_stop(self):
            if post_stop: post_stop(self)

    CustomPathstrider.__name__ = f"{name}Pathstrider"
    return CustomPathstrider
