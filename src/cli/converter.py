"""
converter module contains command on adhoc converting one or more files.
"""
from os import listdir, path

import click

from netcdfella.conversion import Conversion


@click.command("convert")
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
def convert(directory, output_dir, output_kinds, map_dimension, map_variable):
    """
    Convert a file or files in a directory
    """
    print(f">>> Converting file(s) in path: {directory}")
    conversion_proc = Conversion()
    conversion_proc.document_template.exclude_variables(
        {"timeliness_non_nominal", "flash_id"}
    )
    conversion_proc.enable_output_from_str(output_kinds)
    if map_dimension != "" and map_variable != "":
        conversion_proc.set_map_vars(map_dimension, map_variable)
    if path.isfile(directory):
        conversion_proc.convert_document(directory)
    elif path.isdir(directory):
        documents = [doc for doc in listdir(directory)
                     if path.isfile(path.join(directory, doc))]
        print(f"    ***Running conversion for documents: {documents}")
        for doc in documents:
            conversion_proc.convert_document(doc)
