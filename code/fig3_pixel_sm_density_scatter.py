# all sm density scatter

import os
import pandas as pd
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr

def metric(y_predict, y):
    r, p_value = pearsonr(y.values, y_predict)
    bias = np.mean(y_predict - y.values)
    rmse = np.sqrt(mean_squared_error(y.values, y_predict))
    ubrmse = np.sqrt((rmse ** 2 - bias ** 2))
    return [r,p_value,bias,rmse, ubrmse]

# data path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path1 =  path_base + 'data//fig3//'
path_sv = path_base + 'fig'

# metrics
sm_all = pd.read_csv(path1 + 'insitu_pixel_sm_all.csv')

# figure 1
# scatter density
fig_label = ["(a) PGML","(b) ESA CCI","(c) SMOS-IC","(d) SMOS L3","(e) SMAP DCA","(f) SMAP SCAV", "(g) SMAP-IB", "(h) ERA5-Land"]
sm_products = ['pgml_sm','esa_cci_sm','smos_ic_sm','smos_l3_sm','smap_dca_sm','smap_scav_sm','smap_ib_sm','era5_land_sm']


fig, axes = plt.subplots(2, 4,
                         figsize=(12, 5.5),
                         constrained_layout=True)

for i, ax in enumerate(axes.flat):
    # get data
    insitu_sm = sm_all["insitu_sm"]
    sm_select = sm_products[i]
    estimated_sm = sm_all[sm_select]
    # remove nan
    sm_data = pd.DataFrame({'insitu_sm': insitu_sm, 'estimated_sm': estimated_sm})
    sm_data = sm_data.dropna().reset_index(drop=True)
    valid_number = sm_data.shape[0]
    # print(valid_number)
    if sm_data.shape[0] < 100:
        continue
    # metrics
    [r, p_value, bias, rmse, ubrmse] = metric(sm_data["estimated_sm"], sm_data["insitu_sm"])
    # plot
    hb = ax.hexbin(insitu_sm, estimated_sm, gridsize=100, cmap='jet', mincnt=1, vmin=0, vmax = 50)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1.2)
    ax.set_xlabel('In-situ SM ($m^3$/$m^3$)', fontsize=10)
    ax.set_ylabel('Estimated SM ($m^3$/$m^3$)', fontsize=10)
    ax.grid(False)
    ax.set_ylim(0, 0.9)
    ax.set_xlim(0, 0.9)
    ax.set_xticks(np.arange(0, 1, 0.2))
    ax.set_yticks(np.arange(0, 1, 0.2))
    # note
    ax.set_title(fig_label[i],fontsize=10)
    ax.text(0.51, 0.65, f"$R$={r:.3f}\nBias={bias:.3f}\nRMSE={rmse:.3f}\nubRMSE={ubrmse:.3f}",
             fontsize=8, color='black', bbox=dict(facecolor='white', edgecolor='black'))

# colorbar
cbar = fig.colorbar(hb, ax=axes.ravel().tolist(), orientation='vertical',pad=0.01, aspect=40,shrink=0.7)
cbar.set_ticks(np.arange(0, 51, 10))
cbar.set_label("Sample size", fontsize=10)
cbar.ax.tick_params(labelsize=10)

# save
plt.show()
# plt.savefig(path_sv + f"3_1_pixel_sm_scatter_density.png", dpi=300)
# plt.close()

