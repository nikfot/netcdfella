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
        "test_read_netcdf checks if a netcdf file can be read."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()

    def test_to_ascii(self):
        "test_to_ascii writes a netcdf as ascii."
        doc_path = path.join(path.dirname(__file__), "test_netcdf4.nc")
        test_doc = NetCDF("test", doc_path)
        test_doc.read()
        test_doc.to_ascii()
