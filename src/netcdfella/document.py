"""
Document module defines documents that get manipulated by netcdfella.
"""
from functools import partial
from os import path

import matplotlib.colors as clrs
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

    def get_dim(self, name):
        "get_dim returns a dimension by name"
        for dim in self.dimensions:
            if dim.name == name:
                return dim

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

    def to_img_scatter(self, title, dim_name, longitude_name,
                       latitude_name, variable_name, resolution="i",
                       latitude0=0, img_ext="png", plot_samples=3,
                       height=35786000, sphere=(6378137, 6356752.3142),
                       dot_scale=0.01, dot_transparency=0.2, color="magenta",
                       output_path="./", name_suffix="_scatter"):
        "to_jpeg converts a netcdf image to jpeg"
        map = self._create_map("geos", title, resolution,
                               latitude0, height, sphere)
        lons, lats = map(self.get_dim(dim_name).get_variable(longitude_name),
                         self.get_dim(dim_name).get_variable(latitude_name))
        map.scatter(lons, lats, latlon=False,
                    s=dot_scale*self.get_dim(dim_name)
                                    .get_variable(variable_name),
                    c=color,
                    alpha=dot_transparency)
        plot_samples = self._get_variable_samples(dim_name,
                                                  variable_name,
                                                  plot_samples)
        for a in plot_samples:
            map.scatter([], [], c=color, alpha=1, s=dot_scale * a,
                        label=str(a) + " "+variable_name)
        plt.legend(scatterpoints=1, frameon=True,
                   markerscale=2, labelspacing=1, loc=3)
        plt.title(title)
        plt.savefig(output_path+title+name_suffix+"."+img_ext)

    def to_img_marks(self, title, longitude_name, latitude_name,
                     variable_name, img_ext="png", resolution="i",
                     latitude0=0, height=35786000, dot_scale=10,
                     sphere=(6378137, 6356752.3142), dot_transparency=0.2,
                     marker="x", color="b", output_path="./",
                     name_suffix="_marks"):
        """
        Creates an image with marks on the map.
        """
        map = self._create_map("geos", title, resolution,
                               latitude0, height, sphere)
        lons, lats = map(self.dataset[longitude_name][:],
                         self.dataset[latitude_name][:])
        map.scatter(lons, lats, marker=marker, color=color)
        plt.title(title)
        plt.savefig(output_path+title+name_suffix+"."+img_ext)

    def _create_map(self, kind, title, resolution, latitude0, height, sphere):
        "Creates the instance of a basemap."
        if kind == "geos":
            map = GeoStationaryMap(title, resolution, latitude0)
        map.set_sat_height(height).set_sphere(sphere).create_map()
        map.draw()
        return map

    def _get_variable_samples(self, dimension, variable, samples):
        """
        _get_variable_samples returns some samples of the variable from
        smaller to bigger value.
        """
        var = self.get_dim(dimension).get_variable(variable)
        var.sort()
        split_ar = np.split(np.array(var), samples)
        sample_vals = []
        for ar in split_ar:
            sample_vals.append(ar[len(ar)//2])
        return sample_vals

    class Dimension:
        "Dimension describes each dimension of a netcdf file."

        def __init__(self, name, size):
            self.name = name
            self.size = size
            self.variables = {}

        def add_variables(self, name, variable):
            "adds variable data from netcdf file as dictionary."
            self.variables[name] = variable

        def get_variable(self, name):
            "returns the variable of a dimension"
            return self.variables[name]
