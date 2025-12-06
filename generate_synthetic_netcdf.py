import xarray as xr
import numpy as np
import pandas as pd

# Dimensions
time = pd.date_range("2025-12-06", periods=3)
lat = np.linspace(-10, 10, 20)
lon = np.linspace(-10, 10, 20)

# Generate random data
reflectivity = np.random.rand(len(time), len(lat), len(lon)) * 50  # dBZ
velocity = np.random.rand(len(time), len(lat), len(lon)) * 20 - 10  # m/s

# Create Dataset
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

# Save to NetCDF
ds.to_netcdf("sample_4d.nc")
print("Created sample_4d.nc with 2 variables and 3 time steps")
