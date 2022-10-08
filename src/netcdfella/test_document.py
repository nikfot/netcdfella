"""
Documents' module unit tests.
"""
import unittest
from os import path

from netcdfella.document import Document, NetCDF


class TestDocument(unittest.TestCase):
    """
    The test for class Document.
    """

    def test_constructor(self):
        "test_constructor checks if the Document gets initialized correctly."
        test_doc = Document("test", "/")
        self.assertEqual(test_doc.name, "test")
        self.assertEqual(test_doc.path, "/")
        self.assertTrue(isinstance(test_doc, Document))

    def test_read(self):
        "test_read checks if a netcdf file can be read."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()

    def test_get_dim(self):
        "test_get_dim returns the dimension of a netcdf file."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.get_dim("flashes")

    def test__get_variable_samples(self):
        "test_get_variable_samples tests the return of sample values."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc._get_variable_samples("flashes", "radiance", 5)

    def test_to_ascii(self):
        "test_to_ascii writes a netcdf as ascii."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.to_ascii()

    def test_to_img_scatter(self):
        """
        This function takes a list of x and y coordinates
        and a list of colors and plots them on a scatter
        plot.
        """
        "test_to_ascii writes a netcdf as ascii."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.to_img_scatter("title", "flashes",
                                "longitude", "latitude", "radiance")

    def test_to_img_marks(self):
        """
        This function takes a list of x and y coordinates scatters
        marks on the map plot.
        """
        "test_to_ascii writes a netcdf as ascii."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.to_img_marks("title", "longitude", "latitude", "radiance")

    def test_to_graph(self):
        "test_to_graph checks the function to_graph."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.to_graph()
