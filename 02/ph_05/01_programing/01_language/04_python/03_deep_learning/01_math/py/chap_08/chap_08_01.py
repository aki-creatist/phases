# リスト8-1　年収グラフを描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd

# salary.csv読み込み
dat = pd.read_csv('salary.csv', encoding='SHIFT-JIS')

# データをセット
x = dat['年齢']
y = dat['年収']

# グラフを描画
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

# リスト8-2　差分グラフを描画する

# データ数
cnt = len(dat)

# 差分をとる
diff_y = []
for i in range(0, cnt-1):
    diff_y.append(y[i+1] - y[i])

# グラフを描画
plt.plot(x[1:], diff_y)
plt.grid(color='0.8')
plt.show()