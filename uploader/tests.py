# uploader/tests.py
import tempfile
import os
from django.test import TestCase, Client
from django.urls import reverse
from netCDF4 import Dataset
import numpy as np

from .models import NetCDFFile

def create_temp_netcdf_file():
    """Helper function to create a temporary NetCDF file and return its path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
    tmp_path = tmp.name
    tmp.close()  # Close immediately so netCDF4 can write to it on Windows

    with Dataset(tmp_path, "w", format="NETCDF4") as ds:
        # Create dimensions
        ds.createDimension("time", 2)
        ds.createDimension("lat", 3)
        ds.createDimension("lon", 3)

        # Create variables
        times = ds.createVariable("time", "f4", ("time",))
        lats = ds.createVariable("lat", "f4", ("lat",))
        lons = ds.createVariable("lon", "f4", ("lon",))
        reflectivity = ds.createVariable("reflectivity", "f4", ("time", "lat", "lon"))

        # Fill with test data
        times[:] = [0, 1]
        lats[:] = [-10, 0, 10]
        lons[:] = [-10, 0, 10]
        reflectivity[:, :, :] = np.random.rand(2, 3, 3) * 50

    return tmp_path

class NetCDFUploadTests(TestCase):
    """Unit tests for the NetCDF file upload and view."""

    def setUp(self):
        """Set up a test client."""
        self.client = Client()
        self.temp_files = []

    def tearDown(self):
        """Clean up temporary files after each test."""
        for path in self.temp_files:
            if os.path.exists(path):
                os.unlink(path)
        self.temp_files = []

    def test_upload_netcdf_file(self):
        """Test uploading a NetCDF file via the view."""
        tmp_path = create_temp_netcdf_file()
        self.temp_files.append(tmp_path)

        with open(tmp_path, "rb") as f:
            response = self.client.post(reverse("upload_netcdf"), {"file": f})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(NetCDFFile.objects.exists())

    def test_uploaded_file_data_available_in_context(self):
        """Test that the view returns variables, selected variable, and metadata in context."""
        tmp_path = create_temp_netcdf_file()
        self.temp_files.append(tmp_path)

        with open(tmp_path, "rb") as f:
            response = self.client.post(reverse("upload_netcdf"), {"file": f})

        context = response.context
        self.assertIsNotNone(context["variables"])
        self.assertIn("reflectivity", context["variables"])
        self.assertEqual(context["selected_var"], "reflectivity")
        self.assertIsNotNone(context["metadata"])
        self.assertIn("dimensions", context["metadata"])
        self.assertIn("variables", context["metadata"])
        self.assertIn("times", context["metadata"])

    def test_plot_html_in_context(self):
        """Test that the Plotly heatmap HTML is returned in context."""
        tmp_path = create_temp_netcdf_file()
        self.temp_files.append(tmp_path)

        with open(tmp_path, "rb") as f:
            response = self.client.post(reverse("upload_netcdf"), {"file": f})

        context = response.context
        self.assertIsNotNone(context["plot_html"])
        self.assertIn("<div", context["plot_html"])
