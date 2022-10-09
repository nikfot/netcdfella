"""
This is the entrypoint to netcdfella app.
"""
import click

from cli import converter, server, watcher


@click.group("nefctl")
def cli():
    """nefctl is the cli for netcdfella.
    Use it to convert netcdf files to
    ASCII and jpeg.
    """


def main():
    "main is the entrypoint to netcdfella app"
    cli.add_command(watcher.watch)
    cli.add_command(server.serve)
    cli.add_command(converter.convert)
    cli(prog_name="nefctl")


if __name__ == "__main__":
    main()
