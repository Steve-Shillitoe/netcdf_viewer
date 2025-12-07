# tests.py
# ------------------------
# Unit tests for the Django NetCDF uploader app
# These tests check that the upload form works, files are processed correctly,
# and the correct data is passed to the template.
# Comments are added for beginners to explain each step.

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import NetCDFFile
import xarray as xr
import numpy as np
import pandas as pd
import io

class NetCDFUploadTests(TestCase):
    """
    Test case for the NetCDF upload and visualization app.
    Each method tests one piece of functionality.
    """

    def setUp(self):
        """
        setUp runs before each test method.
        Here we create a test client and an in-memory NetCDF file
        so we can simulate file uploads without needing actual files on disk.
        """
        # Django test client simulates browser requests (like a mini-browser)
        self.client = Client()

        # --- Create small test data for our NetCDF file ---
        time = pd.date_range("2025-12-06", periods=2)  # 2 time steps
        lat = np.linspace(-10, 10, 5)  # 5 latitude points
        lon = np.linspace(-10, 10, 5)  # 5 longitude points

        # Random data for reflectivity and velocity
        reflectivity = np.random.rand(len(time), len(lat), len(lon)) * 50
        velocity = np.random.rand(len(time), len(lat), len(lon)) * 20 - 10

        # Create an xarray Dataset (similar to a NetCDF file)
        ds = xr.Dataset(
            {
                "reflectivity": (["time", "lat", "lon"], reflectivity),
                "velocity": (["time", "lat", "lon"], velocity)
            },
            coords={
                "time": time,
                "lat": lat,
                "lon": lon
            }
        )

        # --- Create an in-memory file ---
        # io.BytesIO() is like a "fake file" in memory
        self.nc_bytes = io.BytesIO()
        ds.to_netcdf(self.nc_bytes)  # Save Dataset into this in-memory file
        self.nc_bytes.seek(0)  # Reset pointer to the start of the file

        # --- Wrap in Django UploadedFile for POST request ---
        # SimpleUploadedFile simulates a user uploading a file in a browser
        self.uploaded_file = SimpleUploadedFile(
            "test.nc",           # The filename that will appear in the upload
            self.nc_bytes.read(), # Read bytes from our in-memory NetCDF file
            content_type="application/x-netcdf"  # MIME type of the file
        )

    def test_upload_form_renders(self):
        """
        Test that the upload page loads correctly.
        """
        response = self.client.get(reverse("upload_netcdf"))
        self.assertEqual(response.status_code, 200)  # Page loads successfully
        self.assertContains(response, "<form")       # Page contains a <form> element

    def test_upload_file_creates_model_instance(self):
        """
        Test that uploading a NetCDF file creates a NetCDFFile model instance.
        """
        response = self.client.post(
            reverse("upload_netcdf"),
            {"file": self.uploaded_file},
            follow=True
        )

        # Check that the file is saved in the database
        nc_files = NetCDFFile.objects.all()
        self.assertEqual(nc_files.count(), 1)
        self.assertEqual(nc_files[0].file.name.endswith("test.nc"), True)

        # Check that the response contains the plot HTML
        self.assertContains(response, "plot_html")

    def test_uploaded_file_data_available_in_context(self):
        """
        Test that the view returns variables, selected variable, and metadata
        in the template context after uploading a file.
        """
        response = self.client.post(
            reverse("upload_netcdf"),
            {"file": self.uploaded_file},
            follow=True
        )

        # The context contains the uploaded file instance
        self.assertIn("nc_file_instance", response.context)

        # The context should contain plottable variables
        variables = response.context["variables"]
        self.assertIn("reflectivity", variables)
        self.assertIn("velocity", variables)

        # Selected variable should be in the context
        self.assertIn("selected_var", response.context)
        self.assertIn(response.context["selected_var"], variables)

        # Metadata should be available
        self.assertIn("metadata", response.context)
        self.assertIn("dimensions", response.context["metadata"])
        self.assertIn("variables", response.context["metadata"])

    def test_time_index_selection(self):
        """
        Test that selecting a specific time index works.
        """
        response = self.client.post(
            reverse("upload_netcdf"),
            {
                "file": self.uploaded_file,
                "variable": "reflectivity",
                "time_idx": "1"  # Select the second time step
            },
            follow=True
        )

        # Check that the selected time index is correct in the context
        self.assertEqual(response.context["selected_time_idx"], 1)

    def test_heatmap_plot_generated(self):
        """
        Test that the plotly heatmap HTML is generated after uploading a file.
        """
        response = self.client.post(
            reverse("upload_netcdf"),
            {"file": self.uploaded_file},
            follow=True
        )

        # The plot_html should be present in the context
        self.assertIn("plot_html", response.context)
        self.assertTrue(len(response.context["plot_html"]) > 0)  # Non-empty string

