# Hovmöller diagrams

import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

# set path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path1 =  path_base + 'data//fig6//'
path_sv = path_base + 'fig'

# get sm averaged data
files = sorted([f for f in os.listdir(path1) if f.endswith("lat_monthly.npz")])

# label
fig_label = ["(a) PGML","(b) ESA CCI","(c) SMOS-IC","(d) SMOS L3","(e) SMAP DCA","(f) SMAP SCAV", "(g) SMAP-IB", "(h) ERA5-Land"]
# plot sm lat
fig, axes = plt.subplots(4, 2,
                         figsize=(8,9),
                         constrained_layout=True)
for i, ax in enumerate(axes.flat):
    # data
    dataset = np.load(path1+files[i], allow_pickle=True)
    lat = dataset["lat"]
    date_list = dataset["date_list"]
    date_list_num = mdates.date2num(date_list)
    sm_lat_all = dataset["sm_lat_all"]
    sm_valid = dataset["sm_valid_all"]
    sm_lat_all[sm_valid<10] = np.nan
    # plot
    mesh = ax.pcolormesh(date_list_num.T, lat, sm_lat_all,
                         cmap='jet_r',#'Spectral'
                         shading='auto',vmin=0, vmax=0.5)
    ax.set_ylim(-60,85)
    ax.set_yticks([-50,-23,0,23,50])
    ax.set_yticklabels([f'{int(lat)}°' if lat == 0 else (f'{int(lat)}°N' if lat > 0 else f'{abs(int(lat))}°S') for lat in ax.get_yticks()])
    ax.set_xlim(mdates.date2num(datetime(2015, 4, 1)), mdates.date2num(datetime(2023, 12, 31)))
    x_ticks = [mdates.date2num(datetime(year, 7, 1)) for year in range(2015, 2024, 2)]  # 每两年标记
    ax.set_xticks(x_ticks)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b%Y'))
    ax.set_title(fig_label[i], fontsize=10, color='black')

    # ax.text(mdates.date2num(datetime(2015, 6, 1)), 85, fig_label[i], fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))

# colorbar
cbar = fig.colorbar(mesh, ax=axes.ravel().tolist(), orientation='horizontal', pad=0.01, aspect=50,shrink=0.7)
cbar.set_label("SM ($m^3$/$m^3$)", fontsize=10)
cbar.ax.tick_params(labelsize=10)
cbar.set_ticks(np.arange(0, 0.51, 0.1))
plt.show()
# save
# plt.savefig(path_sv + f"2_1_sm_change_lat_time.png", dpi=600)
# plt.close()
