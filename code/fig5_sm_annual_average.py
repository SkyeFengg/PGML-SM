# Figure
# Annual average sm of all sm products

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

# set path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path1 =  path_base + 'data//fig5//'
path_sv = path_base + 'fig//'

# get sm averaged data
files = sorted([f for f in os.listdir(path1) if f.endswith("sm_1523.nc")])
# variable
variable_name = 'average_sm'
# colorbar
sm_cmap =  mcolors.LinearSegmentedColormap.from_list("custom_cmap",
                                                     ['darkorange','yellow', 'yellowgreen','green', 'turquoise','blue','darkblue'])

# label
fig_label = ["(a) PGML","(b) ESA CCI","(c) SMOS-IC","(d) SMOS L3","(e) SMAP DCA","(f) SMAP SCAV", "(g) SMAP-IB", "(h) ERA5-Land"]
# plot sm
fig, axes = plt.subplots(4, 2,
                         figsize=(9, 9),
                         constrained_layout=True,
                         subplot_kw={'projection': ccrs.PlateCarree()})

for i, ax in enumerate(axes.flat):
    # data
    data = nc_variable_value(path1+files[i], variable_name)
    valid = nc_variable_value(path1+files[i], 'sm_valid_number')
    # data[data<0.02] = np.nan
    # data[valid<100] = np.nan
    lat = nc_variable_value(path1+files[i], "lat_center")
    lon = nc_variable_value(path1+files[i], "lon_center")
    # plot
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    # ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
    ax.set_extent([-180, 180, -65, 85], crs=ccrs.PlateCarree())
    ax.set_xticks(np.arange(-180, 181, 60))
    ax.set_yticks([-50,-23,0,23,50])
    ax.set_xticklabels([f'{int(lon)}°' if lon == 0 else (f'{int(lon)}°E' if lon > 0 else f'{abs(int(lon))}°W') for lon in ax.get_xticks()])
    ax.set_yticklabels([f'{int(lat)}°' if lat == 0 else (f'{int(lat)}°N' if lat > 0 else f'{abs(int(lat))}°S') for lat in ax.get_yticks()])
    mesh = ax.pcolormesh(lon, lat, data,
                         transform=ccrs.PlateCarree(),
                         cmap= sm_cmap,vmin=0, vmax=0.6)
    ax.set_title(fig_label[i], fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))
# colorbar
cbar = fig.colorbar(mesh, ax=axes.ravel().tolist(), orientation='horizontal', pad=0.01, aspect=50,shrink=0.7)
cbar.set_label("SM ($m^3$/$m^3$)", fontsize=10)
cbar.ax.tick_params(labelsize=10)
cbar.set_ticks(np.arange(0, 0.61, 0.1))
# plt.show()
# save
plt.savefig(path_sv + f"fig5_sm_annual_average.png", dpi=300)
plt.close()
