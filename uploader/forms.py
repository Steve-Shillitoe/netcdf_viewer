# uploader/forms.py

# Import Django's forms module, which provides tools to create HTML forms easily
from django import forms

# Import the NetCDFFile model that we defined in models.py
# This model represents the NetCDF files stored in the database
from .models import NetCDFFile

# --------------------------------------------------------------------------
# Define a form class for uploading NetCDF files
# --------------------------------------------------------------------------
# A Django form is a Python class that describes the fields you want
# in your HTML form, as well as how to validate the submitted data.
class NetCDFUploadForm(forms.ModelForm):
    # ----------------------------------------------------------------------
    # Meta class tells Django which model the form is based on
    # ----------------------------------------------------------------------
    class Meta:
        # Link the form to the NetCDFFile model
        model = NetCDFFile

        # Specify which fields from the model we want to include in the form
        # In this case, we only want the 'file' field so the user can upload a NetCDF file
        fields = ['file']

# --------------------------------------------------------------------------
# How this works:
# --------------------------------------------------------------------------
# 1. Django will automatically generate an HTML form with a file input.
# 2. When the user selects a file and submits the form, Django will validate it.
# 3. If the form is valid, we can then save the uploaded file to the database
#    using form.save(), which creates a NetCDFFile instance.
# 4. The form can be rendered in a template with {{ form }}.
