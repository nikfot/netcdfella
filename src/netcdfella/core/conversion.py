"""
conversion module provides the tools around converions.
"""
from os import path

from netcdfella.core.document import NetCDF


class Conversion:
    """
    Conversion is the class about the converion process.
    """

    def __init__(self, output_path="./", input_format="nc"):
        self.input_kind = input_format
        self.document_template = None
        self.output_path = output_path
        self._create_ascii = False
        self._create_scatter_map = False
        self._create_graph = False
        self._create_marks_map = False
        self.map_dimension = None
        self.map_variable = None
        self.map_longitude = None
        self.map_latitude = None
        self.__init_document_template()

    def __init_document_template(self):
        "initializes the document kind template."
        if self.input_kind == "nc":
            self.document_template = NetCDF("template", "temlate")

    def enable_scatter_map(self):
        """
        enables the conversion to scatter map.
        """
        self._create_scatter_map = True

    def enable_marks_map(self):
        """
        enables the conversion to marks map.
        """
        self._create_marks_map = True

    def set_map_vars(
        self, dimension=None, variable=None, longitude="longitude", latitude="latitude"
    ):
        "sets the variables for a map."
        self.map_dimension = dimension
        self.map_variable = variable
        self.map_longitude = longitude
        self.map_latitude = latitude

    def enable_ascii(self):
        "enables the conversion to ascii."
        self._create_ascii = True

    def enable_graph(self):
        "enables the conversion to graph."
        self._create_graph = True

    def convert_document(self, document):
        "converts a document to the preselected format."
        _, file_extension = path.splitext(document)
        if file_extension.replace(".", "") != self.input_kind:
            return
        if self.input_kind == "nc":
            document = NetCDF(path.basename(document), document)
            document.read()
            if self._create_ascii:
                print(f"    *** [ converting {document.name} to ascii ]")
                document.to_ascii()
            if self._create_graph:
                print(f"    *** [ converting {document.name} to graph ]")
                document.to_graph()
            if self._create_scatter_map:
                print(f"    *** [ converting {document.name} to scatter map ]")
                document.to_img_scatter(
                    document.name,
                    self.map_dimension,
                    self.map_longitude,
                    self.map_latitude,
                    self.map_variable,
                )
            if self._create_marks_map:
                print(f"    *** [ converting {document.name} to marks map ]")
                document.to_img_marks(
                    document.name,
                    self.map_dimension,
                    self.map_longitude,
                    self.map_latitude,
                    self.map_variable,
                )

    def enable_output_from_str(self, output_kinds):
        """
        Enable kinds from a comma separated string of output kinds.
        For exampe 'ascii,graph'.
        """
        kinds = output_kinds.strip().split(",")
        for k in kinds:
            if k == "ascii":
                self.enable_ascii()
            if k == "graph":
                self.enable_graph()
            if k == "scatter":
                self.enable_scatter_map()
            if k == "marks":
                self.enable_marks_map()
