from typing import Optional

import typer

from emitunes.api.app import AppBuilder
from emitunes.cli import CliBuilder
from emitunes.config.builder import ConfigBuilder
from emitunes.config.errors import ConfigError
from emitunes.console import FallbackConsoleBuilder
from emitunes.datatunes.migrator import DatatunesMigrator
from emitunes.server import Server

cli = CliBuilder().build()


@cli.command()
def main(
    config_file: Optional[typer.FileText] = typer.Option(
        None,
        "--config-file",
        "-C",
        dir_okay=False,
        help="Configuration file.",
    ),
    config_overrides: Optional[list[str]] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration entries.",
    ),
) -> None:
    """Main entry point."""

    console = FallbackConsoleBuilder().build()

    try:
        config = ConfigBuilder(config_file, config_overrides).build()
    except ConfigError as e:
        console.print("Failed to load config!")
        console.print_exception()
        raise typer.Exit(1) from e

    try:
        app = AppBuilder(config).build()
    except Exception as e:
        console.print("Failed to build app!")
        console.print_exception()
        raise typer.Exit(2) from e

    try:
        DatatunesMigrator(config).migrate()
    except Exception as e:
        console.print("Failed to apply datatunes migrations!")
        console.print_exception()
        raise typer.Exit(3) from e

    try:
        server = Server(app, config)
        server.run()
    except Exception as e:
        console.print("Failed to run server!")
        console.print_exception()
        raise typer.Exit(4) from e


if __name__ == "__main__":
    cli()
