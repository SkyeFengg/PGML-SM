# model improvement - sample sensitivity

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
sm_train_data = pd.read_excel(path1 + 'Finetune_vs_scratch.xlsx')
x = sm_train_data["Training Size"]
r_fine = sm_train_data["finetuned_r_mean"]
r_fine_std = sm_train_data["finetuned_r_std"]
r_pre = sm_train_data["scratch_r_mean"]
r_pre_std = sm_train_data["scratch_r_std"]

rmse_fine = sm_train_data["finetuned_rmse_mean"]
rmse_fine_std = sm_train_data["finetuned_rmse_std"]
rmse_pre = sm_train_data["scratch_rmse_mean"]
rmse_pre_std = sm_train_data["scratch_rmse_std"]

# figure 1
fig, axes = plt.subplots(2, 1, figsize=(4, 3.3), sharex=True, gridspec_kw={'hspace': 0})
ax = axes[0]
bar_width = 0.3
x_pos = np.arange(len(x))
ax.bar(x_pos - bar_width / 2, r_pre, width=bar_width, color='#80B1D3', alpha=0.8, label='Pre-train',yerr=r_pre_std, capsize=3)
ax.bar(x_pos + bar_width / 2, r_fine, width=bar_width, color='#F0D490', alpha=0.8, label='Fine-tune',yerr=r_fine_std, capsize=3)
ax.set_ylabel("$R$", fontsize=10)
ax.set_ylim(0.45, 1.05)
ax.set_yticks([0.5, 0.7, 0.9])
ax.grid(False)
ax.set_title("(b) Sample size sensitivity", fontsize=10)
ax.legend(fontsize=10, loc='upper center', frameon=False, facecolor='none', ncol=2)

ax = axes[1]
ax.bar(x_pos - bar_width / 2, rmse_pre, width=bar_width, color='#80B1D3', alpha=0.8, label='Pre-train',yerr=rmse_pre_std, capsize=3)
ax.bar(x_pos + bar_width / 2, rmse_fine, width=bar_width, color='#F0D490', alpha=0.8, label='Fine-tune',yerr=rmse_fine_std, capsize=3)
ax.set_ylabel('RMSE ($m^3/m^3$)', fontsize=10)
ax.set_ylim(0.04, 0.13)
ax.set_yticks([0.04, 0.08, 0.12])
ax.grid(False)

labels = [('{:.2f}'.format(val)).rstrip('0').rstrip('.') for val in x*100]
plt.xticks(x_pos, labels=labels, fontsize=10)
plt.xlabel('Percentage of sample size (%)',fontsize=10)

plt.tight_layout()
plt.show()
# plt.savefig(path_sv + f"2_2_pgml_sample_size_bar.png", dpi=600)
# plt.close()


