import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors

def nc_variable_value(file_name,variable_name):
    dataset = nc.Dataset(file_name, "r")
    variable = dataset.variables[variable_name][:]
    variable = np.ma.filled(variable, fill_value=np.nan)
    variable = np.array(variable)
    return variable

# colorbar
sm_cmap =  mcolors.LinearSegmentedColormap.from_list("custom_cmap",
                                                     ['darkorange','yellow', 'yellowgreen','green', 'turquoise','blue','darkblue'])

# Define the path
path = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github\data\PGML_SM_daily' + os.sep

# Define the filename
nc_filename = path + 'PGML_SM_20170709_V2.nc'

# Open the NetCDF file in read mode
dataset = nc.Dataset(nc_filename, "r")

for var_name in dataset.variables:
    var = dataset.variables[var_name]
    print(f"Variable Name: {var_name}")
    print(f"Dimensions: {var.dimensions}")
    print(f"Shape: {var.shape}")
    print("-" * 40)

# Extract latitude and longitude
lat = dataset.variables['lat_center'][:]
lon = dataset.variables['lon_center'][:]
lat = np.array(lat)
lon = np.array(lon)

# Plot
# sm
sm = nc_variable_value(nc_filename, 'pgml_sm')
# qc
qc = nc_variable_value(nc_filename, 'qc')
qc1 = (qc >> 0) & 1 # land cover
qc2 = (qc >> 1) & 1 # frozen
qc3 = (qc >> 2) & 1 # dense vegetation, vwc>kg/m2
qc4 = (qc >> 3) & 1 # soil water capacity
sm[(qc1 == 1) | (qc2 == 1) | (qc4 == 1)] = np.nan

if len(sm.shape) == 2:
    plt.figure(figsize=(10, 5))

    # Create a map projection
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.set_title(f"Spatial Distribution of PGML SM")

    # Add features to the map
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
    ax.set_extent([-180, 180, -60, 85], crs=ccrs.PlateCarree())

    # Plot the variable data
    mesh = ax.pcolormesh(lon, lat, sm, transform=ccrs.PlateCarree(), cmap=sm_cmap,vmin=0, vmax=0.6)

    cbar = plt.colorbar(mesh, ax=ax, orientation='vertical')
    cbar.set_label("SM ($m^3$/$m^3$)", fontsize=10)
    cbar.ax.tick_params(labelsize=10)
    cbar.set_ticks(np.arange(0, 0.61, 0.1))
    plt.show()

# Close the dataset
dataset.close()
