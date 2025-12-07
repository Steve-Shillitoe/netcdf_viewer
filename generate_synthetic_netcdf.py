# Import the necessary libraries
import xarray as xr  # For working with multi-dimensional labeled data
import numpy as np   # For numerical operations, arrays, and random numbers
import pandas as pd  # For handling dates and times easily

# --------------------------------------------------------------------------
# Define the dimensions of the dataset
# --------------------------------------------------------------------------
# 'time' dimension: 3 consecutive dates starting from 2025-12-06
time = pd.date_range("2025-12-06", periods=3)

# 'lat' dimension: 20 points evenly spaced from -10 to 10 degrees latitude
lat = np.linspace(-10, 10, 20)

# 'lon' dimension: 20 points evenly spaced from -10 to 10 degrees longitude
lon = np.linspace(-10, 10, 20)

# --------------------------------------------------------------------------
# Generate random data for the variables
# --------------------------------------------------------------------------
# 'reflectivity': random values between 0 and 50 (typical units: dBZ)
# Shape = (time, lat, lon)
reflectivity = np.random.rand(len(time), len(lat), len(lon)) * 50

# 'velocity': random values between -10 and +10 m/s
# Shape = (time, lat, lon)
velocity = np.random.rand(len(time), len(lat), len(lon)) * 20 - 10

# --------------------------------------------------------------------------
# Create an xarray Dataset
# --------------------------------------------------------------------------
# xarray Dataset is like a dictionary of variables, where each variable
# has labeled dimensions (time, lat, lon in this case)
ds = xr.Dataset(
    data_vars={
        # Assign the 3D arrays to variables with their corresponding dimensions
        "reflectivity": (["time", "lat", "lon"], reflectivity),
        "velocity": (["time", "lat", "lon"], velocity)
    },
    coords={
        # Define the coordinates for each dimension
        "time": time,
        "lat": lat,
        "lon": lon
    }
)

# --------------------------------------------------------------------------
# Save the Dataset to a NetCDF file
# --------------------------------------------------------------------------
# NetCDF is a common file format for storing multi-dimensional scientific data
ds.to_netcdf("sample_4d.nc")

# Print a message to confirm the file was created
print("Created sample_4d.nc with 2 variables and 3 time steps")

# --------------------------------------------------------------------------
# HOW TO RUN THIS SCRIPT FROM THE COMMAND LINE
# --------------------------------------------------------------------------
# 1. Make sure you have Python installed (version 3.8+ recommended)
#    You can check by running: python --version
#
# 2. Install the required packages if you haven't already:
#    pip install xarray numpy pandas netCDF4
#
# 3. Save this script to a file, e.g., "create_sample_netcdf.py"
#
# 4. Open a terminal or command prompt, navigate to the folder
#    where the script is saved, e.g., using cd path/to/folder
#
# 5. Run the script with:
#    python create_sample_netcdf.py
#
# 6. After running, you should see a file called "sample_4d.nc"
#    in the same folder, which contains the sample data.
