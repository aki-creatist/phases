# リスト7-6　散布図を描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd

# データ読み込み
dat = pd.read_csv('score.csv', encoding='SHIFT-JIS')

# 散布図
plt.scatter(dat['数学'], dat['理科'])
plt.axis('equal')
plt.show()

# 3.2　共分散と相関係数

import numpy as np
correlation = np.corrcoef(dat['数学'], dat['理科']) # 相関係数を求める
correlation[0,1]  # 画面に表示