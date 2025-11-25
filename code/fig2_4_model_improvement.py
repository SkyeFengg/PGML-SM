# figure about model improvement
# step by step

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

# data path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path = path_base + 'data//fig2//'
path_sv = path_base + 'fig//'

# metrics
sm_step_data = pd.read_excel(path + 'stepwise-improvement.xlsx')
sm_step_data = sm_step_data.rename(columns={'Unnamed: 0': 'item'})

# ==== R metrics ====
r_means = sm_step_data.loc[sm_step_data["item"] == "R Mean"].drop(columns="item").values.flatten()

r_std = sm_step_data.loc[sm_step_data["item"] == "R STD"].drop(columns="item").values.flatten()

# ==== RMSE metrics ====
rmse_means = sm_step_data.loc[sm_step_data["item"] == "RMSE Mean"].drop(columns="item").values.flatten()
rmse_std = sm_step_data.loc[sm_step_data["item"] == "RMSE STD"].drop(columns="item").values.flatten()

# ==== 计算增量 ====
r_increments = np.diff(r_means, prepend=0)
r_increments[r_increments < 0] = 0
r_bottoms = np.insert(np.cumsum(r_increments[:-1]), 0, 0)

rmse_reductions = np.diff(rmse_means, prepend=0)
rmse_reductions[rmse_reductions > 0] = 0
rmse_reductions = np.abs(rmse_reductions)
rmse_bottoms = np.zeros_like(rmse_means)
for i in range(len(rmse_means) - 1):
    rmse_bottoms[i] = rmse_means[i + 1]

# ==== plot set ====
categories = ["ML", "+KGE Loss", "+ Pre-train", "+ Fine-tune"]
colors = ["#1f77b4", "#52bedb", "#b0e3b0", "#ffdf66"]

fig, axes = plt.subplots(2, 1, figsize=(4, 3.5), sharex=True, gridspec_kw={'hspace': 0})

# ==== R ====
ax = axes[0]
for i in range(len(categories)):
    yerr = r_std[i]
    if i == 0:
        ax.bar(categories[i], r_means[i], color=colors[i], yerr=yerr, capsize=3)
        ax.text(i, r_means[i] + 0.012, f"{r_means[i]:.3f}", ha = 'center', fontsize = 8)
    else:
        ax.bar(categories[i], r_means[i], color=colors[i], yerr=yerr, capsize=3)
        ax.text(i, r_means[i] + 0.012, f"+{r_increments[i]:.3f}", ha='center', fontsize=8)

ax.set_title("(d) Contribution of each step (n=10,000)", fontsize=10)
ax.set_ylabel("$R$", fontsize=10)
ax.set_ylim(0.7, 0.81)
ax.set_yticks([0.70, 0.75, 0.80])
ax.grid(False)

# ==== RMSE ====
ax = axes[1]
for i in range(len(categories)):
    yerr = rmse_std[i]
    if i == 0:
        ax.bar(categories[i], rmse_means[i], color=colors[i], yerr=yerr, capsize=3)
        ax.text(i, rmse_means[i] + 0.002, f"{rmse_means[i]:.3f}", ha = 'center', fontsize = 8)
    else:
        ax.bar(categories[i], rmse_means[i], color=colors[i], yerr=yerr, capsize=3)
        ax.text(i, rmse_means[i] + 0.002, f"-{rmse_reductions[i]:.3f}", ha='center', fontsize=8)

ax.set_ylabel('RMSE ($m^3/m^3$)', fontsize=10)
ax.set_ylim(0.06, 0.085)
ax.set_yticks([0.06, 0.07, 0.08])
ax.grid(False)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=30, ha="right", fontsize=10)

plt.tight_layout(pad = 1)
# plt.show()
plt.savefig(path_sv + f"fig2_4_pgml_sm_bar.png", dpi=300)
plt.close()