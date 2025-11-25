
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
path_info =  path_base + 'data//pixel_csv//info//'
path_sm = path_base + 'data//pixel_csv//csv//'
path_sv = path_base + 'fig//'

# ====================================================================
# pixel info
insitu_info = pd.read_csv(path_info + 'insitu_pixel_daily_all_data_info.csv')

insitu_pixel_sm_all = pd.DataFrame(columns=["pgml_sm", "insitu_sm"])

for i in range(0, len(insitu_info)):
    pixel_id = insitu_info.loc[i, "pixel_id"]
    data = pd.read_csv(path_sm + pixel_id + '.csv')
    cols = ["pgml_sm", "insitu_sm"]
    data = data.dropna(subset = cols, ignore_index = True, how = 'any')
    mask = data['date'] >= 20240101
    data = data.loc[mask].reset_index(drop = True)
    #
    if len(data) < 1:
        continue

    # organize all sm
    sm_all = pd.DataFrame(columns=["pgml_sm","insitu_sm"] )
    sm_all['pgml_sm'] = data['pgml_sm']
    sm_all["insitu_sm"] = data["insitu_sm"]
    sm_all_cleaned = sm_all.dropna(axis=0, how='all').reset_index(drop=True)
    insitu_pixel_sm_all = pd.concat([insitu_pixel_sm_all, sm_all_cleaned], ignore_index = True)

    del sm_all,data
    print(i, pixel_id)

# ====================================================================

# figure 1
# scatter density
# PGML
x = insitu_pixel_sm_all["insitu_sm"]
y = insitu_pixel_sm_all["pgml_sm"]

plt.figure(figsize=(3.7, 3))
plt.subplots_adjust(bottom = 0.145, left = 0.149)
hb = plt.hexbin(x, y, gridsize=150, cmap='jet', mincnt=1,vmin=0, vmax=25)
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
plt.text(0.01, 0.58, f"n = {int(len(x)):,}\n$R$={r:.3f}\nBias={bias:.3f}\nRMSE={rmse:.3f}\nubRMSE={ubrmse:.3f}",
             fontsize=9, color='black', bbox=dict(facecolor='none', edgecolor='none'))
plt.title(f"(b) Independent validation", fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))

# plt.show()
plt.savefig(path_sv + f"fig2_2_pgml_sm_scatter_independent.png", dpi=300)
plt.close()


