from pathlib import Path
import subprocess
import pluggy

from imperium.pathstrider import BasePathstrider, PATHSTRIDER_MARKER
from imperium.utils import write_to_env

hookimpl = pluggy.HookimplMarker(PATHSTRIDER_MARKER)


class DefaultPathstrider(BasePathstrider):
    """
    Default Pathstrider implementation.

    Lifecycle:
    - init_plugin: prepare configuration and environment file
        * pre_init()   -> runs before env/config setup
        * post_init()  -> runs after env/config setup
    - start_plugin: launch docker-compose
        * pre_start()  -> runs before docker compose starts
        * post_start() -> runs after docker compose has started
    - stop_plugin: shut down docker-compose
        * pre_stop()   -> runs before docker compose stops
        * post_stop()  -> runs after docker compose has stopped
    """

    def __init__(self):
        self.logger = None
        self.config = None
        self.base_dir: Path | None = None
        self.name: str = "Pathstrider"
        self.docker_compose_file: str | None = None

    # -------------------
    # INIT PHASE
    # -------------------
    @hookimpl
    def init_plugin(self, logger, config, base_dir):
        self.logger = logger
        self.config = config
        self.base_dir = base_dir
        if not self.docker_compose_file: self.docker_compose_file = str(self.base_dir / "docker-compose.yml")

        self.logger.log(f"{self.name} intializing...")
        self.pre_init()

        self.config.update({"base_dir": self.base_dir})
        write_to_env(env_path=base_dir / ".env", config_dict=self.config)

        self.post_init()
        self.logger.log(f"{self.name} initialized.")

    def pre_init(self):
        """Lifecycle hook: runs before environment/config is set up."""
        pass

    def post_init(self):
        """Lifecycle hook: runs after environment/config is written."""
        pass

    # -------------------
    # START PHASE
    # -------------------
    @hookimpl
    def start_plugin(self):
        self.logger.log(f"{self.name} starting...")
        self.pre_start()

        self._start_docker()

        self.post_start()
        self.logger.log(f"{self.name} started successfully.")

    def pre_start(self):
        """Lifecycle hook: runs before docker compose is started."""
        pass

    def post_start(self):
        """Lifecycle hook: runs after docker compose has started successfully."""
        pass

    def _start_docker(self):
        start_docker_cmd = ["docker", "compose", "-f", self.docker_compose_file, "up", "-d"]

        try:
            self.logger.log(f"Starting docker for {self.name} with: {' '.join(start_docker_cmd)}")
            subprocess.run(start_docker_cmd, check=True)
            self.logger.log(f"Docker for {self.name} started successfully.")
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Error starting docker for {self.name}: {e}")

    # -------------------
    # STOP PHASE
    # -------------------
    @hookimpl
    def stop_plugin(self):
        self.logger.log(f"{self.name} stopping...")
        self.pre_stop()

        self._stop_docker()

        self.post_stop()
        self.logger.log(f"{self.name} stopped successfully.")

    def pre_stop(self):
        """Lifecycle hook: runs before docker compose is stopped."""
        pass

    def post_stop(self):
        """Lifecycle hook: runs after docker compose has been stopped."""
        pass

    def _stop_docker(self):
        stop_docker_cmd = ["docker", "compose", "-f", self.docker_compose_file, "down"]

        try:
            self.logger.log(f"Stopping docker for {self.name} with: {' '.join(stop_docker_cmd)}")
            subprocess.run(stop_docker_cmd, check=True)
            self.logger.log(f"Docker for {self.name} stopped.")
        except subprocess.CalledProcessError as e:
            self.logger.log(f"Error while stopping docker for {self.name}: {e}")
