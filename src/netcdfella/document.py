"""
Document module defines documents that get manipulated by netcdfella.
"""
from functools import partial
from os import path

import matplotlib.pyplot as plt
import numpy as np
from ncplot import view
from netCDF4 import Dataset

from netcdfella.maps import GeoStationaryMap


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
        self.dataset = None

    def exclude_variables(self, exclusions):
        "exclude netcdf variables from netcdf file reading."
        self.excluded_variables.update(exclusions)

    def read(self):
        "Reads the contents of a netcdf file."
        self.dataset = Dataset(self.path)
        # pylint: disable=not-an-iterable
        for dim in self.dataset.dimensions:
            # pylint: disable=unsubscriptable-object
            new_dimension = self.Dimension(
                self.dataset.dimensions[dim].name,
                self.dataset.dimensions[dim].size
            )
            # pylint: disable=no-member
            for k in self.dataset.variables.keys():
                if k not in self.excluded_variables:
                    # pylint: disable=unsubscriptable-object
                    new_dimension.add_variables(k,
                                                self.dataset.variables[k][:])
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

    def to_graph(self, variable=None):
        "to_graph creates graphical representations of variables."
        if self.output_path is not None:
            out_dir = self.output_path + path.splitext(self.path)[0] + ".html"
        else:
            out_dir = path.splitext(self.path)[0] + ".html"
        view(self.path, var=variable, out=out_dir, quadmesh=True)

    def to_img_scatter(self, title, longitude_name, latitude_name,
                       variable_name, resolution="i", latitude0=0,
                       height=35786000, sphere=(6378137, 6356752.3142),
                       dot_scale=10, dot_transparency=0.2):
        "to_jpeg converts a netcdf image to jpeg"
        map = self._create_map("geos", title, resolution,
                               latitude0, height, sphere)
        lons, lats = map(self.dataset[longitude_name][:],
                         self.dataset[latitude_name][:])
        map.scatter(lons, lats, latlon=False,
                    s=dot_scale*np.log2(self.dataset[variable_name][:]),
                    cmap='summer', c=np.log2(self.dataset[variable_name][:]),
                    alpha=0.2)
        for a in [100, 300, 500]:
            map.scatter([], [], c='r', alpha=0.5, s=a,
                        label=str(a) + ' radiance')
        plt.legend(scatterpoints=1, frameon=False,
                   labelspacing=1, loc='lower left')
        plt.title(title)
        plt.savefig("2m_temp.png")

    def to_img_marks(self, title, longitude_name, latitude_name,
                     variable_name, resolution="i", latitude0=0,
                     height=35786000, sphere=(6378137, 6356752.3142),
                     dot_scale=10, dot_transparency=0.2):
        """
        Creates an image with marks on the map.
        """
        map = self._create_map("geos", title, resolution,
                               latitude0, height, sphere)
        lons, lats = map(self.dataset[longitude_name][:],
                         self.dataset[latitude_name][:])
        map.scatter(lons, lats, marker='x', color='b')
        plt.title(title)
        plt.savefig("test_markers.png")

    def _create_map(self, kind, title, resolution, latitude0, height, sphere):
        "Creates the instance of a basemap."
        if kind == "geos":
            map = GeoStationaryMap(title, resolution, latitude0)
        map.set_sat_height(height).set_sphere(sphere).create_map()
        map.draw()
        return map

    class Dimension:
        "Dimension describes each dimension of a netcdf file."

        def __init__(self, name, size):
            self.name = name
            self.size = size
            self.variables = {}

        def add_variables(self, name, variable):
            "adds variable data from netcdf file as dictionary."
            self.variables[name] = variable
