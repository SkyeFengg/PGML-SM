# Calculate SM anomaly

import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
import pandas as pd
from datetime import datetime

def nc_variable_value(file_name,variable_name):
    dataset = nc.Dataset(file_name, "r")
    variable = dataset.variables[variable_name][:]
    variable = np.ma.filled(variable, fill_value=np.nan)
    variable = np.array(variable)
    return variable

# set path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path1 =  path_base + 'data//fig7//'
path_sv = path_base + 'fig'

# monthly files
files1 = sorted([f for f in os.listdir(path1) if f.startswith("pgml_sm_2018")])
files2 = sorted([f for f in os.listdir(path1) if f.startswith("cci_sm_2018")])
files_selected1 = files1[0]
files_selected2 = files2[0]

# get lat lon
lat1 = nc_variable_value(path1+files1[0], "lat_center")
lon1 = nc_variable_value(path1+files1[0], "lon_center")
lat2 = nc_variable_value(path1+files2[0], "lat_center")
lon2 = nc_variable_value(path1+files2[0], "lon_center")

lat_all = [52.19, 55.92, 52.34]
lon_all = [6.42, 8.91, 0.80]


# plot
# label
fig_label = ["(a) PGML SM Anomaly (July 2018)","(b) PGML SM (July 2018)", "(c) ESA CCI SM (July 2018)"]
sm_anomaly_cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap",
                                                    ['#533104','#90560D','#C58E3C','#E7CF93','#F6EED9','#DCEFED','#98D7CE','#47A49A','#086D65','#003C30'])
sm_cmap =  mcolors.LinearSegmentedColormap.from_list("custom_cmap",
                                                     ['darkorange','yellow', 'yellowgreen','green', 'turquoise','blue','darkblue'])

bins1 = np.linspace(-50, 50, 11)
norm1 = mcolors.BoundaryNorm(bins1, sm_cmap.N)

# figure 2
fig, axes = plt.subplots(1, 3,
                         figsize=(8, 3),
                         constrained_layout=True,
                         subplot_kw={
                             'projection': ccrs.LambertConformal(central_longitude=10, central_latitude=55)})

for i, ax in enumerate(axes.flat):
    month_str = files_selected1[12:14]
    # sm data
    sm_mean = nc_variable_value(path1 + 'pgml_sm_' + month_str + '.nc', 'average_sm')
    sm_month = nc_variable_value(path1 + files_selected1, 'average_sm')
    sm_anomaly = (sm_month - sm_mean)
    sm_anomaly_perc = (sm_anomaly / sm_mean) * 100
    sm_anomaly_perc = np.ma.masked_invalid(sm_anomaly_perc)

    cci_sm_mean = nc_variable_value(path1 + files_selected2, 'average_sm')


    # plot
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.set_extent([-25, 40, 34, 72], ccrs.PlateCarree())



    if i == 0:
        mesh = ax.pcolormesh(lon1, lat1, sm_anomaly_perc,
                             transform=ccrs.PlateCarree(),
                             cmap=sm_anomaly_cmap, norm=norm1)
        cbar1 = fig.colorbar(mesh, ax=ax, orientation='horizontal',
                             extend='both', boundaries=bins1, pad=0.02, aspect=25, shrink=0.8)
        cbar1.set_ticks([-40, -20, 0, 20, 40])
        cbar1.set_label("PGML SM Anomaly (%)", fontsize=10)
        cbar1.ax.tick_params(labelsize=10)
        # plt.show()
    elif i == 1:
        mesh = ax.pcolormesh(lon1, lat1, sm_mean,
                             transform=ccrs.PlateCarree(),cmap=sm_cmap,vmin=0, vmax=0.6)
        cbar2 = fig.colorbar(mesh, ax=ax, orientation='horizontal',
                             pad=0.02, aspect=25, shrink=0.8)
        cbar2.set_ticks(np.arange(0, 0.61, 0.1))
        cbar2.set_label("SM ($m^3$/$m^3$)", fontsize=10)
        cbar2.ax.tick_params(labelsize=10)
    else:
        mesh = ax.pcolormesh(lon2, lat2, cci_sm_mean,
                             transform=ccrs.PlateCarree(), cmap=sm_cmap,vmin=0, vmax=0.6)
        cbar3 = fig.colorbar(mesh, ax=ax, orientation='horizontal',
                             pad=0.02, aspect=25, shrink=0.8)
        cbar3.set_ticks(np.arange(0, 0.61, 0.1))
        cbar3.set_label("SM ($m^3$/$m^3$)", fontsize=10)
        cbar3.ax.tick_params(labelsize=10)

    scatter = ax.scatter(lon_all, lat_all,  # cmap=color_map[i]
                         color='red', s=10, edgecolors='red',
                         transform=ccrs.PlateCarree())

    ax.set_title(f"{fig_label[i]}", fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))


plt.show()
# save
# plt.savefig(path_sv + f"7_pgml_sm_anomaly.png", dpi=300)
# plt.close()
