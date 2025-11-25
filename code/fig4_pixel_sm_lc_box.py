# all sm metrics

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# data path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path1 =  path_base + 'data//fig3+4//'
path_sv = path_base + 'fig//'

# figure 1
# 1 metrics for 6 product
fig_label = ["(a) $R$","(b) Bias","(c) RMSE","(d) ubRMSE"]
legend_label = ["PGML","ESA CCI","SMOS L3","SMAP DCA","SMAP SCAV", "ERA5-Land"]
metrics = ["r","bias","rmse","ubrmse"]
metric_label = ["$R$", "Bias ($m^3$/$m^3$)", "RMSE ($m^3$/$m^3$)", "ubRMSE ($m^3$/$m^3$)"]
sm_products = ['pgml_sm','esa_cci_sm','smos_l3_sm','smap_dca_sm','smap_scav_sm','era5_land_sm',]

sm_colors = {
    'pgml_sm': '#FF1030',
    'esa_cci_sm': '#2BBF62',
    'smos_l3_sm': '#1F3FD2',
    'smap_dca_sm': '#00BFFF',
    'smap_scav_sm': '#A22BB9',
    'era5_land_sm': '#E69500'
}
group_color = ['#FF1030','#2BBF62','#1F3FD2','#00BFFF','#A22BB9','#E69500']

y_min = [0,-0.21,0.01,0.01]
y_max = [1.1,0.38,0.38,0.14]
y_tick = [np.arange(0.3, 1, 0.3),np.arange(-0.2, 0.4, 0.2),np.arange(0, 0.41, 0.1),np.arange(0, 0.21, 0.05)]

land_cover_map = {
    # 0: "WB",
    1: "ENF",
    # 2: "EBF",
    # 3: "DNF",
    4: "DBF",
    5: "MXF",
    # 6: "CSH",
    7: "OSH",
    8: "WSA",
    9: "SAV",
    10: "GRL",
    # 11: "PWL",
    12: "CRL",
    # 13: "URB",
    # 14: "CRM",
    # 15: "SNI",
    16: "BSV"
}

for i in range(0,len(metrics)):
    metric = metrics[i]
    dataset = pd.read_csv(path1 + 'insitu_pixel_daily_' + metric + '.csv')
    dataset = dataset.dropna()
    dataset = dataset.reset_index(drop=True)
    valid_site = dataset.shape[0]

    # organize
    dataset_long = pd.melt(dataset, id_vars=['pixel_id', 'land_cover_types'],
                      value_vars=sm_products,var_name='SMProduct', value_name=metric)

    # land cover
    dataset_long["land_cover"] = dataset_long["land_cover_types"].map(land_cover_map)
    land_cover_unique = [land_cover_map[lc] for lc in sorted(land_cover_map.keys())]
    counts = dataset_long.groupby("land_cover")["pixel_id"].nunique().to_dict()

    # plot
    plt.figure(figsize=(9, 2.2))
    # boxplot
    ax = sns.boxplot(x="land_cover", y=metric,hue="SMProduct",data=dataset_long,
                      order=land_cover_unique,
                      palette=sm_colors,
                      width = 0.83,
                      gap = 0.25,
                      fill = True,
                      whis = (5,95),
                      linewidth = 1,
                      # notch = True,
                      legend = 'auto',
                      flierprops={"marker": "."}, fliersize=0,
                      medianprops={"linewidth": 2})

    for patch in ax.patches:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))
        patch.set_edgecolor((r, g, b, a))

    for line in ax.lines:
        xdata = line.get_xdata()[0]
        group_xdata = range(0,9,1)
        gap_xdata1 = [-0.45,-0.3,0.15,0,0.15,0.25]
        gap_xdata2 = [-0.3,-0.15,0,0.15,0.3,0.6]
        for p in range(0,len(group_xdata)):
            for q in range(0,len(gap_xdata1)):
                if (group_xdata[p]+0.5>xdata>group_xdata[p]-0.5) and (gap_xdata2[q] > (xdata - group_xdata[p]) > gap_xdata1[q]):
                    line.set_color(group_color[q])
    # legend color
    handles, labels = ax.get_legend_handles_labels()
    for n, handle in enumerate(handles):
        handle.set_edgecolor(sm_colors[labels[n]])

    ax.legend().set_visible(False)

    ticks_labels = [f"{lc}\n(n={counts.get(lc, 0)})" for lc in land_cover_unique]
    plt.xticks(ticks = range(len(land_cover_unique)), labels = ticks_labels, fontsize = 10)
    plt.xlabel("IGBP land cover types")

    # if i==0:
    #     ax.legend(handles=handles,labels=legend_label,loc='lower center', bbox_to_anchor=(0.5, 1.15), fontsize=10,
    #               frameon=False,facecolor='none',ncol=6)
    # else:
    #     ax.legend().set_visible(False)

    # if i ==3:
        # ax.legend().set_visible(False)
        # ticks_labels = [f"{lc}\n(n={counts.get(lc, 0)})" for lc in land_cover_unique]
        # plt.xticks(ticks=range(len(land_cover_unique)), labels=ticks_labels,fontsize=10)
        # plt.xlabel("IGBP land cover types")
    # else:
    #     ax.set_xticks(range(len(land_cover_unique)))
    #     ax.set_xticklabels([])
    #     ax.set_xlabel("")


    plt.ylabel(metric_label[i],fontsize=10)
    plt.yticks(y_tick[i], fontsize=10)
    plt.ylim(y_min[i], y_max[i])
    plt.title(fig_label[i],fontsize=10, color='black', bbox=dict(facecolor='none', edgecolor='none'))
    plt.tight_layout()
    # plt.show()
    plt.savefig(path_sv + f"4_{i+1}_pixel_{metric}_boxplot.png", dpi=600)
    plt.close()
