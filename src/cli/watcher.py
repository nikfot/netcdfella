"""
watcher module implements the commands for watching a directory
for file changes.
"""

import click

from netcdfella.conversion import Conversion
from qnotify.watcher import Watcher


@click.command("watch")
@click.argument("directory", default="./")
@click.option(
    "-o",
    "--output-dir",
    default="./",
    help="set the output directory for converted files.",
)
def watch(directory, output_dir):
    """
    Watch a directory for any new netcdf file and convert it.
    """
    print(directory, output_dir)
    conversion_proc = Conversion(output_format="asc")
    conversion_proc.document_template.exclude_dimensions(
        {"timeliness_non_nominal", "flash_id"}
    )
    watcher = Watcher("new", directory, conversion_proc.convert_document)
    watcher.set_notifier()
    watcher.start()
