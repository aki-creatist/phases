# リスト3-1　体重グラフを描画する

#%matplotlib inline
import matplotlib.pyplot as plt

# データ
x = [1, 2, 3, 4, 5, 6, 7]
y = [64.3, 63.8, 63.6, 64.0, 63.5, 63.2, 63.1]

# グラフを描画
plt.plot(x, y)        # 折れ線を描画
plt.grid(color='0.8') # グリッドを表示
plt.show()            # 画面に表示