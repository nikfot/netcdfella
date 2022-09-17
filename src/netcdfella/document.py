"""
Document module defines documents that get manipulated by netcdfella.
"""
from functools import partial
from os import path

from netCDF4 import Dataset


class Document:
    """
    Document is the generic form of netcdfella documents.
    """

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.input_kind = None
        self.output_path = None
        self.output_kind = None

    def set_output_kind(self, output_kind):
        "Set the format type for the converted document"
        self.output_kind = output_kind

    def set_input_kind(self, input_kind):
        "Set the format type for the input document"
        self.input_kind = input_kind

    def set_output_path(self, output_path):
        "Set the output path for converted files."
        self.output_path = output_path


class NetCDF(Document):
    "NetCDF class contains usefull info for NetCDF files."

    def __init__(self, name, doc_path):
        Document.__init__(self, name, doc_path)
        self.excluded_variables = {"timeliness_non_nominal"}
        self.dimensions = []

    def exclude_variables(self, exclusions):
        "exclude netcdf variables from netcdf file reading."
        self.excluded_variables.update(exclusions)

    def read(self):
        "Reads the contents of a netcdf file."
        dataset = Dataset(self.path)
        # pylint: disable=not-an-iterable
        for dim in dataset.dimensions:
            # pylint: disable=unsubscriptable-object
            new_dimension = self.Dimension(
                dataset.dimensions[dim].name, dataset.dimensions[dim].size
            )
            # pylint: disable=no-member
            for k in dataset.variables.keys():
                if k not in self.excluded_variables:
                    # pylint: disable=unsubscriptable-object
                    new_dimension.add_variables(k, dataset.variables[k][:])
            self.dimensions.append(new_dimension)

    def to_ascii(self):
        "to_ascii converts a netcdf document to ascii."
        open_utf8 = partial(open, encoding="UTF-8")
        ascii_file = path.splitext(self.path)[0] + ".asc"
        ascii_file = open_utf8(ascii_file, "w")
        first_line = ""
        for _, dim in enumerate(self.dimensions):
            first_line = "@DIMENSION: " + dim.name + " "
            ascii_file.write(first_line)
            ascii_file.write("\n")
            second_line = ""
            for key, _ in dim.variables.items():
                second_line = second_line + key + " "
            ascii_file.write("@VARIABLES: " + second_line)
            ascii_file.write("\n")
            ascii_file.write("@DATA\n")
            for i in range(dim.size):
                current_line = ""
                for _, var in dim.variables.items():
                    current_line = current_line + f"{var[i]}" + " "
                ascii_file.write(current_line)
                ascii_file.write("\n")
        ascii_file.close()

    class Dimension:
        "Dimension describes each dimension of a netcdf file."

        def __init__(self, name, size):
            self.name = name
            self.size = size
            self.variables = {}

        def add_variables(self, name, variable):
            "adds variable data from netcdf file as dictionary."
            self.variables[name] = variable
