# uploader/models.py

# Import Django's models module, which allows us to define database tables as Python classes
from django.db import models

# --------------------------------------------------------------------------
# Define a database model for storing NetCDF files
# --------------------------------------------------------------------------
# In Django, a "model" is a Python class that represents a database table.
# Each attribute of the class represents a column in the table.

class NetCDFFile(models.Model):
    # 'file' is a column that stores the uploaded NetCDF file
    # FileField tells Django this is a file upload field
    # 'upload_to' specifies the folder inside MEDIA_ROOT where files will be saved
    file = models.FileField(upload_to='netcdf/')

    # 'uploaded_at' is a column that stores the timestamp of when the file was uploaded
    # auto_now_add=True means Django will automatically set this value when a new record is created
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------------------------------------------------
    # This method defines how the object will appear as a string
    # Useful in the Django admin and when printing the object
    # ----------------------------------------------------------------------
    def __str__(self):
        # Return the filename as the string representation of this object
        return str(self.file)

# --------------------------------------------------------------------------
# How this works:
# --------------------------------------------------------------------------
# 1. Each NetCDFFile object corresponds to a row in the database table.
# 2. When you upload a file via a form, Django creates a new NetCDFFile object and stores it in the database.
# 3. 'file' stores the file itself (in the MEDIA_ROOT/netcdf/ folder) and the database stores the path.
# 4. 'uploaded_at' automatically records when the file was uploaded.
# 5. You can see these files and timestamps in the Django admin panel.
