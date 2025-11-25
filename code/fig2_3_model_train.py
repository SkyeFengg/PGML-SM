
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
sm_train_data = pd.read_excel(path + 'sample_sensitivity.xlsx')
x = sm_train_data["Sample_size"]
r_fine = sm_train_data["F_R Mean"]
r_fine_std = sm_train_data["F_R Std"]
r_pre = sm_train_data["P_R Mean"]
r_pre_std = sm_train_data["P_R Std"]

rmse_fine = sm_train_data["P_RMSE Mean"]
rmse_fine_std = sm_train_data["F_RMSE Std"]
rmse_pre = sm_train_data["P_RMSE Mean"]
rmse_pre_std = sm_train_data["P_RMSE Std"]

# figure 1
fig, axes = plt.subplots(2, 1, figsize=(4, 3.3), sharex=True, gridspec_kw={'hspace': 0})
ax = axes[0]
bar_width = 0.3
x_pos = np.arange(len(x))
ax.bar(x_pos - bar_width / 2, r_pre, width=bar_width, color='#80B1D3', alpha=0.8, label='Pre-train',yerr=r_pre_std, capsize=3)
ax.bar(x_pos + bar_width / 2, r_fine, width=bar_width, color='#F0D490', alpha=0.8, label='Fine-tune',yerr=r_fine_std, capsize=3)
ax.set_ylabel("$R$", fontsize=10)
ax.set_ylim(0.4, 1.05)
ax.set_yticks([0.5, 0.7, 0.9])
ax.grid(False)
ax.set_title("(c) Sample size sensitivity (n=457,681)", fontsize=10)
ax.legend(fontsize=10, loc='upper center', frameon=False, facecolor='none', ncol=2)

# plt.show()

ax = axes[1]
ax.bar(x_pos - bar_width / 2, rmse_pre, width=bar_width, color='#80B1D3', alpha=0.8, label='Pre-train',yerr=rmse_pre_std, capsize=3)
ax.bar(x_pos + bar_width / 2, rmse_fine, width=bar_width, color='#F0D490', alpha=0.8, label='Fine-tune',yerr=rmse_fine_std, capsize=3)
ax.set_ylabel('RMSE ($m^3/m^3$)', fontsize=10)
ax.set_ylim(0.03, 0.14)
ax.set_yticks([0.04, 0.08, 0.12])
ax.grid(False)

labels = [('{:.2f}'.format(val)).rstrip('0').rstrip('.') for val in x*100]
plt.xticks(x_pos, labels=labels, fontsize=10)
plt.xlabel('Percentage of sample size (%)',fontsize=10)

plt.tight_layout()
# plt.show()
plt.savefig(path_sv + f"fig2_3_pgml_sample_size_bar.png", dpi=600)
plt.close()


