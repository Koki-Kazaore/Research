# -*- coding: utf-8 -*-
"""annBasedDispatchModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AZhSsxE5eShVeyMRuPWfgPBKGIn7FWju
"""

# 必要なライブラリのインポート
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score
from sklearn.preprocessing import StandardScaler

# データの読み込み
data = pd.read_csv('opt_base_dispatched_data.csv')
data

"""## 学習用にデータを整形"""

# timestampカラムをdatetime型に変換
data['timestamp'] = pd.to_datetime(data['timestamp'])

# 一日の始まりからの経過分を計算
data['elapsed_time'] = (data['timestamp'] - data['timestamp'].dt.normalize()).dt.total_seconds() / 60

# 元のtimestampカラムを削除（必要に応じて）
data = data.drop('timestamp', axis=1)
data

# ==== パラメータ設定 ==== (2 mins)
M = 3  # 1リクエストあたりの最大候補自転車数
include_no_assignment = True  # 割り当てないクラスを追加
# include_no_assignmentをTrueにした場合、クラス数はM+1となる。

# # 各request_idごとに距離が最小のbikeをassigned=1にする
# def assign_min_distance(df):
#     idx = df['distance_user_bike'].idxmin()
#     df.loc[:, 'assigned'] = 0
#     df.loc[idx, 'assigned'] = 1
#     return df

# data = data.groupby('request_id').apply(assign_min_distance)
# data = data.reset_index(drop=True)

# ==== データのマルチクラス化 ====
# request_idごとにグループ化し、M台分のbike候補を抽出（距離が近い順などのルールでソート）
# 今回は単純にdistance_user_bikeでソートして上位M台を使用。
# M台未満ならダミー行を追加してパディング。
def pad_bikes(group):
    # 距離順にソート
    group = group.sort_values(by='distance_user_bike').reset_index(drop=True)

    # クラスラベルは、assigned=1のbikeが何番目か（0-based）
    assigned_idx = group.index[group['assigned']==1]
    if len(assigned_idx) == 0:
        chosen_class = -1  # 割り当てなし
    else:
        chosen_class = assigned_idx[0]

    # M台に満たない場合はダミー自転車を追加
    while len(group) < M:
        dummy = group.iloc[0:1].copy()
        dummy[['bike_id','bike_current_lon','bike_current_lat','owner_lon','owner_lat','distance_user_bike','assigned']] = 0
        group = pd.concat([group, dummy], ignore_index=True)

    # M台より多ければ上位M台のみ残す
    group = group.iloc[:M]

    # chosen_classがMより大きい場合は上位Mに入っていないので割り当てなし
    if chosen_class >= M or chosen_class == -1:
        if include_no_assignment:
            # no-assignmentクラスをM番目のクラスとする
            final_class = M
        else:
            # no assignmentクラスを設けない場合は、該当なし時はM台の中に1がいないので困るが
            # この場合は単純に一番目のbikeをassigned=1にするなどルールが必要
            # ここでは簡略化のため0番目を強制的に1にする
            final_class = 0
    else:
        final_class = chosen_class

    # 特徴量を整形
    # ユーザ側特徴量は共通
    user_feats = group.loc[0, ['user_current_lon','user_current_lat','user_dest_lon','user_dest_lat','elapsed_time']].values
    # 各bikeの特徴量を縦に並べる
    bike_feats = []
    for i in range(M):
        bike_i = group.iloc[i]
        bike_feats.extend([
            bike_i['bike_current_lon'],
            bike_i['bike_current_lat'],
            bike_i['owner_lon'],
            bike_i['owner_lat'],
            bike_i['distance_user_bike']
        ])
    # user_feats + bike_featsが最終特徴量ベクトル
    # ラベルはfinal_class
    return pd.Series(np.concatenate([user_feats, bike_feats, [final_class]]))

agg_data_backup = data.groupby('request_id').apply(pad_bikes)

# aggデータを1からやり直したい場合
agg_data = agg_data_backup.copy()

agg_data

# カラム名を設定
user_cols = ['user_current_lon','user_current_lat','user_dest_lon','user_dest_lat','elapsed_time']
bike_cols = []
for i in range(M):
    bike_cols += [f'bike{i+1}_current_lon', f'bike{i+1}_current_lat', f'bike{i+1}_owner_lon', f'bike{i+1}_owner_lat', f'bike{i+1}_distance_user_bike']
label_col = ['label']
agg_data.columns = user_cols + bike_cols + label_col

agg_data = agg_data.reset_index(drop=True)

X = agg_data[user_cols + bike_cols].values
y = agg_data['label'].values.astype(int)

# クラス数
num_classes = M+1 if include_no_assignment else M
y_onehot = tf.keras.utils.to_categorical(y, num_classes=num_classes)

# スケーリング
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_onehot, test_size=0.2, random_state=42, stratify=y_onehot)

# ==== モデル構築 (マルチクラス) ====
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)
y_true = np.argmax(y_test, axis=1)

acc = accuracy_score(y_true, y_pred)
print("Test Accuracy:", acc)

# 新規リクエストに対する予測例
# 同様にユーザ特徴＋M台分のバイク特徴を用意し、モデルに入力する
# ここでは適当にダミーで
new_request_user = np.array([-73.95, 40.75, -73.96, 40.76, 600]) # user側5特徴
new_request_bikes = np.random.uniform(-74.0, -73.9, size=M*5) # M台分×5特徴（bike_current_lon, bike_current_lat, owner_lon, owner_lat, distance_user_bike）

new_request_user

new_request_features = np.concatenate([new_request_user, new_request_bikes])
new_request_scaled = scaler.transform([new_request_features])

new_request_scaled

new_prob = model.predict(new_request_scaled)[0]
pred_class = np.argmax(new_prob)

if pred_class < M:
    print(f"このリクエストには bike{pred_class+1} を割り当てるクラスが選ばれました")
else:
    print("このリクエストには割り当てないことが選ばれました (no assignment)")

# モデルを保存する（HDF5形式）
model.save('trained_multiclass_model.h5')

# 保存したモデルは次のようにして使う
"""
from tensorflow.keras.models import load_model

# 保存したモデルの読み込み
loaded_model = load_model('trained_multiclass_model.h5')

# 読み込んだモデルで予測を実行可能
new_prob = loaded_model.predict(new_request_scaled)[0]
pred_class = np.argmax(new_prob)
"""