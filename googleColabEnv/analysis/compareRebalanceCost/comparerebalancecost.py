# -*- coding: utf-8 -*-
"""compareRebalanceCost.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ECuOTvOdnzn0_RwouO7DSOYaJ8uhVPnz

# 概要
各々のモデルを用いて自転車を割り当てた場合のリバランスコストの推移を比較して、モデルの優位性を確認するためのプログラム
"""

import branca.colormap as cm
import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from geopy.distance import geodesic
from pandas import DataFrame
from scipy.interpolate import PchipInterpolator

# データのインポート
df_time_series_neighborhood = pd.read_csv('/content/result_by_neighborhoodBasedDispatchModel.csv')
df_time_series_optimization = pd.read_csv('/content/result_by_optimizationBasedDispatchModel.csv')
df_time_series_random = pd.read_csv('/content/result_by_randomBasedDispatchModel.csv')
df_time_series_withoutStackOpt = pd.read_csv('/content/result_by_withoutStackOptBasedDispatchModel.csv')

print(df_time_series_neighborhood.info())
print(df_time_series_optimization.info())
print(df_time_series_random.info())
print(df_time_series_withoutStackOpt.info())

df_time_series = [
    df_time_series_random,
    df_time_series_neighborhood,
    df_time_series_withoutStackOpt,
    df_time_series_optimization
]

# それぞれのdf_time_serieのrebalance_costカラムの推移を比較する図をプロットする

# まず'time'カラムをdatetimeオブジェクトに変換する。
df_time_series_optimization['time'] = pd.to_datetime(df_time_series_optimization['time'])

# 秒に変換
time = df_time_series_random['time'].values / 1e9
stack_time = df_time_series_optimization['time'].astype('int64') / 1e9

# 補間のための新しい時間データを作成
time_new = np.linspace(time.min(), time.max(), 300)
stack_time_new = np.linspace(stack_time.min(), stack_time.max(), 300)

# PCHIP補間
pchip_rebalance_cost_random = PchipInterpolator(time, df_time_series_random['rebalance_cost'])
rebalance_cost_smooth_random = pchip_rebalance_cost_random(time_new)

pchip_rebalance_cost_neighborhood = PchipInterpolator(time, df_time_series_neighborhood['rebalance_cost'])
rebalance_cost_smooth_neighborhood = pchip_rebalance_cost_neighborhood(time_new)

pchip_rebalance_cost_withoutStackOpt = PchipInterpolator(time, df_time_series_withoutStackOpt['rebalance_cost'])
rebalance_cost_smooth_withoutStackOpt = pchip_rebalance_cost_withoutStackOpt(time_new)

pchip_rebalance_cost_optimization = PchipInterpolator(stack_time, df_time_series_optimization['rebalance_cost'])
rebalance_cost_smooth_optimization = pchip_rebalance_cost_optimization(stack_time_new)

# プロット
fig, ax1 = plt.subplots(figsize=(10, 6))

# 新しい時間データをDateTimeに変換してプロット
time_new_datetime = pd.to_datetime(time_new * 1e9)

# 各モデルのリバランスコストの推移をプロット
plt.plot(time_new_datetime, rebalance_cost_smooth_random, label='Random')
plt.plot(time_new_datetime, rebalance_cost_smooth_neighborhood, label='neighborhood') # Add the other plots back in
plt.plot(time_new_datetime, rebalance_cost_smooth_withoutStackOpt, label='withoutStackOpt')
plt.plot(time_new_datetime, rebalance_cost_smooth_optimization, label='optimization')
# plt.plot(df_time_series_optimization['time'], df_time_series_optimization['rebalance_cost'], label='Optimization')
# plt.plot(df_time_series_random['time'], df_time_series_random['rebalance_cost'], label='Random')
# plt.plot(df_time_series_withoutStackOpt['time'], df_time_series_withoutStackOpt['rebalance_cost'], label='Without Stack Opt')

# 軸ラベル、凡例、タイトルを設定
plt.xlabel('Time')
plt.ylabel('Rebalance Cost')
plt.legend()
plt.grid(True)
plt.title('Comparison of rebalancing costs by model over time')

# グラフを表示
plt.show()

"""## スケールデータ"""

# データのインポート
df_time_series_neighborhood = pd.read_csv('/content/result_by_neighborhoodBasedDispatchModel_50.csv')
df_time_series_optimization = pd.read_csv('/content/result_by_optimizationModelWithCupy_50.csv')
df_time_series_random = pd.read_csv('/content/result_by_randomBasedDispatchModel_50.csv')
df_time_series_withoutStackOpt = pd.read_csv('/content/result_by_withoutStackOptBasedDispatchModel_50.csv')

print(df_time_series_neighborhood.info())
print(df_time_series_optimization.info())
print(df_time_series_random.info())
print(df_time_series_withoutStackOpt.info())

df_time_series = [
    df_time_series_random,
    df_time_series_neighborhood,
    df_time_series_withoutStackOpt,
    df_time_series_optimization
]

# それぞれのdf_time_serieのrebalance_costカラムの推移を比較する図をプロットする

# まず'time'カラムをdatetimeオブジェクトに変換する。
df_time_series_optimization['time'] = pd.to_datetime(df_time_series_optimization['time'])

# 秒に変換
time = df_time_series_random['time'].values / 1e9
stack_time = df_time_series_optimization['time'].astype('int64') / 1e9

# 補間のための新しい時間データを作成
time_new = np.linspace(time.min(), time.max(), 300)
stack_time_new = np.linspace(stack_time.min(), stack_time.max(), 300)

# PCHIP補間
pchip_rebalance_cost_random = PchipInterpolator(time, df_time_series_random['rebalance_cost'])
rebalance_cost_smooth_random = pchip_rebalance_cost_random(time_new)

pchip_rebalance_cost_neighborhood = PchipInterpolator(time, df_time_series_neighborhood['rebalance_cost'])
rebalance_cost_smooth_neighborhood = pchip_rebalance_cost_neighborhood(time_new)

pchip_rebalance_cost_withoutStackOpt = PchipInterpolator(time, df_time_series_withoutStackOpt['rebalance_cost'])
rebalance_cost_smooth_withoutStackOpt = pchip_rebalance_cost_withoutStackOpt(time_new)

pchip_rebalance_cost_optimization = PchipInterpolator(stack_time, df_time_series_optimization['rebalance_cost'])
rebalance_cost_smooth_optimization = pchip_rebalance_cost_optimization(stack_time_new)

# プロット
fig, ax1 = plt.subplots(figsize=(10, 6))

# 新しい時間データをDateTimeに変換してプロット
time_new_datetime = pd.to_datetime(time_new * 1e9)

# 各モデルのリバランスコストの推移をプロット
plt.plot(time_new_datetime, rebalance_cost_smooth_random, label='Random')
plt.plot(time_new_datetime, rebalance_cost_smooth_neighborhood, label='neighborhood') # Add the other plots back in
plt.plot(time_new_datetime, rebalance_cost_smooth_withoutStackOpt, label='withoutStackOpt')
plt.plot(time_new_datetime, rebalance_cost_smooth_optimization, label='optimization')
# plt.plot(df_time_series_optimization['time'], df_time_series_optimization['rebalance_cost'], label='Optimization')
# plt.plot(df_time_series_random['time'], df_time_series_random['rebalance_cost'], label='Random')
# plt.plot(df_time_series_withoutStackOpt['time'], df_time_series_withoutStackOpt['rebalance_cost'], label='Without Stack Opt')

# 軸ラベル、凡例、タイトルを設定
plt.xlabel('Time')
plt.ylabel('Rebalance Cost')
plt.legend()
plt.grid(True)
# plt.title('Comparison of rebalancing costs by model over time')

# グラフを表示
plt.show()

"""## スケールデータ100"""

# データのインポート
df_time_series_neighborhood = pd.read_csv('/content/result_by_neighborhoodBasedDispatchModel_100.csv')
df_time_series_optimization = pd.read_csv('/content/result_by_optimizationModelWithCupy_100.csv')
df_time_series_random = pd.read_csv('/content/result_by_randomBasedDispatchModel_100.csv')
df_time_series_withoutStackOpt = pd.read_csv('/content/result_by_withoutStackOptBasedDispatchModel_100.csv')

print(df_time_series_neighborhood.info())
print(df_time_series_optimization.info())
print(df_time_series_random.info())
print(df_time_series_withoutStackOpt.info())

df_time_series = [
    df_time_series_random,
    df_time_series_neighborhood,
    df_time_series_withoutStackOpt,
    df_time_series_optimization
]

# それぞれのdf_time_serieのrebalance_costカラムの推移を比較する図をプロットする

# まず'time'カラムをdatetimeオブジェクトに変換する。
df_time_series_optimization['time'] = pd.to_datetime(df_time_series_optimization['time'])

# 秒に変換
time = df_time_series_random['time'].values / 1e9
stack_time = df_time_series_optimization['time'].astype('int64') / 1e9

# 補間のための新しい時間データを作成
time_new = np.linspace(time.min(), time.max(), 300)
stack_time_new = np.linspace(stack_time.min(), stack_time.max(), 300)

# PCHIP補間
pchip_rebalance_cost_random = PchipInterpolator(time, df_time_series_random['rebalance_cost'])
rebalance_cost_smooth_random = pchip_rebalance_cost_random(time_new)

pchip_rebalance_cost_neighborhood = PchipInterpolator(time, df_time_series_neighborhood['rebalance_cost'])
rebalance_cost_smooth_neighborhood = pchip_rebalance_cost_neighborhood(time_new)

pchip_rebalance_cost_withoutStackOpt = PchipInterpolator(time, df_time_series_withoutStackOpt['rebalance_cost'])
rebalance_cost_smooth_withoutStackOpt = pchip_rebalance_cost_withoutStackOpt(time_new)

pchip_rebalance_cost_optimization = PchipInterpolator(stack_time, df_time_series_optimization['rebalance_cost'])
rebalance_cost_smooth_optimization = pchip_rebalance_cost_optimization(stack_time_new)

# プロット
fig, ax1 = plt.subplots(figsize=(10, 6))

# 新しい時間データをDateTimeに変換してプロット
time_new_datetime = pd.to_datetime(time_new * 1e9)

# 各モデルのリバランスコストの推移をプロット
plt.plot(time_new_datetime, rebalance_cost_smooth_random, label='Random')
plt.plot(time_new_datetime, rebalance_cost_smooth_neighborhood, label='neighborhood') # Add the other plots back in
plt.plot(time_new_datetime, rebalance_cost_smooth_withoutStackOpt, label='withoutStackOpt')
plt.plot(time_new_datetime, rebalance_cost_smooth_optimization, label='optimization')
# plt.plot(df_time_series_optimization['time'], df_time_series_optimization['rebalance_cost'], label='Optimization')
# plt.plot(df_time_series_random['time'], df_time_series_random['rebalance_cost'], label='Random')
# plt.plot(df_time_series_withoutStackOpt['time'], df_time_series_withoutStackOpt['rebalance_cost'], label='Without Stack Opt')

# 軸ラベル、凡例、タイトルを設定
plt.xlabel('Time')
plt.ylabel('Rebalance Cost')
plt.legend()
plt.grid(True)
# plt.title('Comparison of rebalancing costs by model over time')

# グラフを表示
plt.show()