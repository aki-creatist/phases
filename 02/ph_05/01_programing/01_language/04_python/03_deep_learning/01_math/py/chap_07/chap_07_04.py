# リスト7-7　移動平均グラフを描画

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 気温データの読み込み
dat= pd.read_csv('temperature.csv', encoding='SHIFT-JIS')

n = len(dat)       # データ数
x = range(1, n+1)  # x軸の値（1～データ数）

# 気温
y = dat['平均気温']  # y軸の値（平均気温）
plt.plot(x, y)       # グラフを描画

# 区間数:9 の移動平均
v = np.ones(9)/9.0
y2 = np.convolve(y, v, mode='same')  # 移動平均を求める
plt.plot(x[4:n-4], y2[4:n-4])        # グラフを描画
plt.show()

# リスト7-8　回帰直線を求める

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# データ
x = np.array([23,24,28,24,27,21,18,25,28,20])  # 気温
y = np.array([37,22,62,32,74,16,10,69,83,7])   # ジュースの販売数

# 回帰直線
a, b = np.polyfit(x, y, 1)
y2 = a * x + b
print('傾き: {0}, 切片:{1}'.format(a, b))

# 描画
plt.scatter(x, y)  # 散布図
plt.plot(x, y2)    # 回帰直線
plt.show()

# 気温33度のときの販売数を予測
a * 33 + b