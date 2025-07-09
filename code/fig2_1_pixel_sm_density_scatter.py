# pixel scale density scatter

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
path1 =  path_base + 'data//fig2//'
path_sv = path_base + 'fig'

# metrics
sm_all = pd.read_csv(path1 + 'random_cv_results.csv')
valid_number = sm_all.shape[0]
# figure 1
# scatter density
# PGML
x = sm_all["observation"]
y = sm_all["prediction"]

plt.figure(figsize=(3.7, 3))
plt.subplots_adjust(bottom = 0.145, left = 0.149)
hb = plt.hexbin(x, y, gridsize=150, cmap='jet', mincnt=1,vmin=0, vmax=200)
plt.plot([0, 1], [0,1], 'k--', linewidth=1.2)
plt.xlabel('Measured SM ($m^3$/$m^3$)', fontsize=10)
plt.ylabel('Estimated SM ($m^3$/$m^3$)', fontsize=10)
plt.grid(False)
plt.ylim(0, 0.85)
plt.xlim(0, 0.85)
plt.xticks(np.arange(0, 0.81, 0.2), fontsize=10)
plt.yticks(np.arange(0, 0.81, 0.2), fontsize=10)
cbar = plt.colorbar(hb,pad=0.015,aspect=50)
cbar.set_label('Sample size', fontsize=10)
plt.tight_layout()
[r, p, bias, rmse, ubrmse] = metric(y, x)
plt.text(0.01, 0.58, f"n = {int(valid_number):,}\n$R$={r:.3f}\nBias={bias:.3f}\nRMSE={rmse:.3f}\nubRMSE={ubrmse:.3f}",
             fontsize=9, color='black', bbox=dict(facecolor='none', edgecolor='none'))
plt.title(f"(a) Out of sample validation", fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))

plt.show()
# plt.savefig(path_sv + f"2_1_pgml_sm_all_scatter.png", dpi=300)
# plt.close()


