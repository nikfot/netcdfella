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
@click.option(
    "-k",
    "--output-kinds",
    default="",
    help="set the output kind for conversion.",
)
@click.option(
    "-md",
    "--map-dimension",
    default="",
    help="set the dimenion to use for mapping.",
)
@click.option(
    "-mv",
    "--map-variable",
    default="",
    help="set the variable to use for mapping.",
)
def watch(directory, output_dir, output_kinds, map_dimension, map_variable):
    """
    Watch a directory for any new netcdf file and convert it.
    """
    print(directory, output_dir)
    conversion_proc = Conversion()
    conversion_proc.document_template.exclude_variables(
        {"timeliness_non_nominal", "flash_id"}
    )
    conversion_proc.enable_output_from_str(output_kinds)
    if map_dimension != "" and map_variable != "":
        conversion_proc.set_map_vars(map_dimension, map_variable)
    watcher = Watcher("new", directory, conversion_proc.convert_document)
    watcher.set_notifier()
    watcher.start()
