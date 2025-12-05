# Figure 2
# pixel scale scatter density plot

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
path = path_base + 'data//fig2//'
path_sv = path_base + 'fig//'

# metrics
sm_all = pd.read_csv(path + '5fold_cv_results.csv')
valid_number = sm_all.shape[0]

# figure 1
# scatter density
# PGML
x = sm_all["observation"]
y = sm_all["y_pred"]

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

# plt.show()
plt.savefig(path_sv + f"fig2_1_pgml_sm_scatter_5cv.png", dpi=300)
plt.close()


