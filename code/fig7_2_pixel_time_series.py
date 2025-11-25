import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from functools import reduce

def metric(y_predict, y):
    r, p_value = pearsonr(y.values, y_predict)
    bias = np.mean(y_predict - y.values)
    rmse = np.sqrt(mean_squared_error(y.values, y_predict))
    ubrmse = np.sqrt((rmse ** 2 - bias ** 2))
    return [r,p_value,bias,rmse, ubrmse]

def format_lon(lon):
    if lon == 0:
        return f'{lon:.2f}°'
    elif lon > 0:
        return f'{lon:.2f}°E'
    else:
        return f'{abs(lon):.2f}°W'
def format_lat(lat):
    if lat == 0:
        return f'{lat:.2f}°'
    elif lat > 0:
        return f'{lat:.2f}°N'
    else:
        return f'{abs(lat):.2f}°S'

def expand_date_gaps(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    date_format: str = '%Y%m%d',
    max_gap_days: int = 30
) -> pd.DataFrame:

    # 1.
    tmp = df.copy()
    tmp_date = tmp["date"].astype(str).str[:8]
    tmp['_sm_date'] = pd.to_datetime(tmp_date, format=date_format)
    tmp = tmp[['_sm_date', value_col]].sort_values('_sm_date').reset_index(drop=True)

    # 2.
    parts = []
    for i in range(len(tmp) - 1):
        cur = tmp.iloc[i]
        nxt = tmp.iloc[i+1]
        parts.append(cur.to_frame().T)

        gap = (nxt._sm_date - cur._sm_date).days
        if gap > max_gap_days:
            missing = pd.date_range(
                start=cur._sm_date + pd.Timedelta(days=1),
                end=nxt._sm_date - pd.Timedelta(days=1),
                freq='D'
            )
            parts.append(pd.DataFrame({
                '_sm_date': missing,
                value_col: np.nan
            }))

    parts.append(tmp.iloc[[-1]])

    # 3.
    out = pd.concat(parts, ignore_index=True).sort_values('_sm_date').reset_index(drop=True)
    out[date_col] = out['_sm_date']
    return out[[date_col, value_col]]

land_cover_map = {
    0: "WB",
    1: "ENF",
    2: "EBF",
    3: "DNF",
    4: "DBF",
    5: "MXF",
    6: "CSH",
    7: "OSH",
    8: "WSA",
    9: "SAV",
    10: "GRL",
    11: "PWL",
    12: "CRL",
    13: "URB",
    14: "CRM",
    15: "SNI",
    16: "BSV"
}
climate_map = {# 0: "WB",
    100: "Tropocal",
    200: "Arid",
    300: "Temperate",
    400: "Cold",
    500: "Polar"
}

# set path
path_base = r'C:\Users\au783073\OneDrive - Aarhus universitet\Desktop\Scientific_data\Github' + os.sep
path_info =  path_base + 'data//pixel_csv//info//'
path_sm = path_base + 'data//pixel_csv//csv//'
path_sv = path_base + 'fig//'

# set figure para
sm_color = ['#FF1030','#2BBF62','#1F3FD2','#00BFFF','#A22BB9','#E69500']
start_date = pd.to_datetime('2015-04-01')
end_date = pd.to_datetime('2020-12-31')
note_date = pd.to_datetime('2015-04-10')

# read info
insitu_info = pd.read_csv(path_info + 'insitu_pixel_daily_all_data_info.csv')
site_id_all = insitu_info["pixel_id"]
insitu_info["land_cover"] = insitu_info["land_cover_types"].map(land_cover_map)
insitu_info["climate"] = insitu_info["koppen_climate_5_types"].map(climate_map)

# get network data
pixel_selected = ['742_TWENTE','164_HOBE','43_COSMOS-UK']
title_num = ['(f) C:','(d) A:','(e) B:']


for i in range(0, len(pixel_selected)):

    pixel_id = pixel_selected[i]
    pixel_info = insitu_info[insitu_info["pixel_id"] == pixel_id]
    pixel_info = pixel_info.reset_index(drop=True)

    # read data
    data_all = pd.read_csv(path_sm + pixel_id + ".csv")
    site_data = data_all[["date","insitu_sm","pgml_sm","esa_cci_sm","era5_prep"]]
    site_data = site_data.sort_values('date')
    site_data = site_data.dropna(subset=['insitu_sm'])


    # all match
    site_data1 = site_data.dropna()
    site_data1 = site_data1.reset_index(drop=True)
    insitu_sm1 = site_data1["insitu_sm"]
    pgml_sm1 = site_data1["pgml_sm"]
    other_sm1 = site_data1["esa_cci_sm"]
    sm_date1 = site_data1["date"].astype(str).str[:8]
    sm_date1 = pd.to_datetime(sm_date1, format='%Y%m%d')

    # check in-situ sm nan
    # if missing > 30 day, show nan
    sm_expanded = expand_date_gaps(
        site_data,
        date_col='date',
        value_col='insitu_sm',
        date_format='%Y%m%d',
        max_gap_days=30
    )

#----------------------------------------------------------------------------------------------
    # date
    prep_date = site_data["date"].astype(str).str[:8]
    prep_date = pd.to_datetime(prep_date, format='%Y%m%d')
    sm_date = sm_expanded["date"]

    # data
    insitu_sm = sm_expanded["insitu_sm"]
    prep_data = site_data["era5_prep"]
    pixel_lc = pixel_info["land_cover"]
    pixel_climate = pixel_info["climate"]
    pixel_lat = pixel_info["lat"]
    pixel_lon = pixel_info["lon"]


    # plot
    plt.figure(figsize=(10, 2))
    # 2018
    start_highlight = pd.to_datetime("2018-01-01")
    end_highlight = pd.to_datetime("2018-12-31")
    plt.axvspan(start_highlight, end_highlight, color='wheat')

    plt.plot(sm_date, insitu_sm, '-', label='In-situ SM', color='black', linewidth=1.5, zorder=2)
    plt.plot(sm_date1, pgml_sm1, marker='o', markersize=2, label='PGML',
             markeredgecolor=sm_color[0], markerfacecolor='none', alpha=0.7, linewidth=0, zorder=3)
    plt.plot(sm_date1, other_sm1, marker='o', markersize=2, label='ESA CCI',
             markeredgecolor=sm_color[2], markerfacecolor='none', alpha=0.7, linewidth=0, zorder=3)

    plt.grid(alpha=0)
    plt.ylim(0, 0.65)
    plt.ylabel("SM ($m^3$/$m^3$)")
    plt.yticks(np.arange(0, 0.61, 0.2), fontsize=10)
    plt.xlim(start_date, end_date)  # Set x-axis range from April 2015 to Dec 2024
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b%y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(bymonth=[7]))
    plt.legend(fontsize=8, loc='upper right', frameon=True, facecolor='white', edgecolor='black', ncol=3)
    # plt.show()
    # metric
    x = pgml_sm1[(sm_date1 >= start_highlight) & (sm_date1 <= end_highlight)]
    y = insitu_sm1[(sm_date1 >= start_highlight) & (sm_date1 <= end_highlight)]
    if len(x) < 100:
        continue
    [r, p_value, bias, rmse, ubrmse] = metric(x, y)
    plt.text(note_date, 0.59,
             f"PGML: $R$={r:.3f} Bias={bias:.3f} RMSE={rmse:.3f} ubRMSE={ubrmse:.3f}",
             fontsize=8, color=sm_color[0], bbox=dict(facecolor='none', edgecolor='none'))
    x = other_sm1[(sm_date1 >= start_highlight) & (sm_date1 <= end_highlight)]
    [r, p_value, bias, rmse, ubrmse] = metric(x, y)
    plt.text(note_date, 0.53,
             f"ESA CCI: $R$={r:.3f} Bias={bias:.3f} RMSE={rmse:.3f} ubRMSE={ubrmse:.3f}",
             fontsize=8, color=sm_color[2], bbox=dict(facecolor='none', edgecolor='none'))

    ax2 = plt.gca().twinx()
    ax2.vlines(prep_date, 0, prep_data, color='deepskyblue', alpha=0.5, linewidth=1, zorder=1)
    ax2.tick_params(axis='y', labelcolor='deepskyblue')
    ax2.set_ylabel("Precipitation (mm)", color='deepskyblue')
    ax2.set_ylim(0, 50)
    ax2.set_yticks(np.arange(0, 50, 15))

    valid_number = len(x)

    plt.title(
        f"{title_num[i]} {pixel_id.split('_')[1]} | {format_lat(pixel_lat.iloc[0])} {format_lon(pixel_lon.iloc[0])} | {pixel_lc.iloc[0]} | {pixel_climate.iloc[0]} | n = {int(valid_number)}",
        fontsize=10) #{title_num[i]}


    plt.tight_layout()
    # plt.show()
    plt.savefig(path_sv + f"fig7_{pixel_id}_sm.png", dpi=300)
    plt.close()
    print(pixel_id)
