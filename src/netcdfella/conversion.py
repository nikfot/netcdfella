""" 
conversion module provides the tools around converions.
"""
from os import path

from netcdfella.document import NetCDF


class Conversion:
    """
    Conversion is the class about the converion process.
    """

    def __init__(self, output_format, output_path="./", input_format="nc"):
        self.input_kind = input_format
        self.document_template = None
        self.output_kind = output_format
        self.output_path = output_path
        self.__init_document_template()

    def __init_document_template(self):
        "initializes the document kind template."
        if self.input_kind == "nc":
            self.document_template = NetCDF("template", "temlate")

    def convert_document(self, document):
        "converts a document to the preselected format."
        if self.input_kind == "nc":
            document = NetCDF(path.basename(document), document)
            document.set_output_kind(self.output_kind)
            document.read()
