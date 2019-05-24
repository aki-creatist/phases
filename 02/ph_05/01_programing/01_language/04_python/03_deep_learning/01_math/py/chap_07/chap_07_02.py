# 2.1　分散と標準偏差

import numpy as np
owner = [94, 105, 107, 106, 88]  # 店長のデータ
mean = np.mean(owner)            # 平均
sum = 0
for d in owner:
    sum = sum + (d - mean) #「データ－平均」の合計を求める
sum

# 「データ－平均」の2乗
sum = 0
for d in owner:
    sum = sum + (d - mean)**2  #「データ－平均」の2乗を合計
sum

# 分散と標準偏差
import math
variance = sum / 5          # 分散
stdev = math.sqrt(variance) # 標準偏差
variance, stdev

# リスト7-4　度数分布図を描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd

# データ読み込み
dat = pd.read_csv('onigiri.csv', encoding='SHIFT-JIS')

# 度数分布図
plt.hist(dat['店長'], bins=range(0, 200, 10), alpha=0.5)
plt.hist(dat['太郎'], bins=range(0, 200, 10), alpha=0.5)
plt.show()

# リスト7-5　平均、分散、標準偏差を求める

import numpy as np
print('店長---------')
print('平均:', np.mean(dat['店長']))
print('分散:', np.var(dat['店長']))
print('標準偏差:', np.std(dat['店長']))

print('太郎---------')
print('平均:', np.mean(dat['太郎']))
print('分散:', np.var(dat['太郎']))
print('標準偏差:', np.std(dat['太郎']))

# 2.2　偏差値

# 偏差値の計算
def dev_value(score, mean, stdev):
    return (score - mean) / stdev * 10 + 50

# 4月の偏差値
dev_value(320, 278, 60)

# 9月の偏差値
dev_value(430, 388, 60)
