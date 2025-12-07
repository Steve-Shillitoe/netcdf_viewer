from django.urls import path
from . import views

# --------------------------------------------------------------------------
# URL patterns for the uploader app
# When the root URL ('') is accessed, the upload_netcdf view function is called
# This allows users to upload and visualize NetCDF files
# --------------------------------------------------------------------------

urlpatterns = [
    path('', views.upload_netcdf, name='upload_netcdf'),]
