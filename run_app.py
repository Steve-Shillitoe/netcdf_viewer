import os
import sys

from django.core.management import execute_from_command_line

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netcdf_viewer.settings')

# Start Django server on port 8000
execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:8000"])

