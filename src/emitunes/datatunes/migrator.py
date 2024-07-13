import os
import subprocess

from emitunes.config.models import Config


class DatatunesMigrator:
    """Migrator class for datatunes database migrations."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def _get_command(self) -> list[str]:
        """Get the command to run."""

        return ["prisma", "migrate", "deploy"]

    def _get_connection_string(self) -> str:
        """Get the connection string."""

        return self._config.datatunes.sql.url

    def _get_env(self) -> dict[str, str]:
        """Get the environment variables."""

        env = os.environ.copy()

        return env | {
            "PRISMA_DB_URL": self._get_connection_string(),
        }

    def migrate(self) -> None:
        """Apply migrations."""

        try:
            subprocess.run(
                self._get_command(),
                env=self._get_env(),
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            message = e.stderr.decode() if e.stderr else "Unknown error."
            raise RuntimeError(message) from e
