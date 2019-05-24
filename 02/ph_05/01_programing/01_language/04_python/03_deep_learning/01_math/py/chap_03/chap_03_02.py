# 2.2 関数

y = []
for x in range(1, 11):
    y.append(3 * x - 24)
y

# リスト3-2　y=3x-24 のグラフ

#% matplotlib
inline
import matplotlib.pyplot as plt

# データ
x = list(range(1, 11))  # xの値（1～10）
y = []
for i in range(10):
    y.append(3 * x[i] - 24)  # y = 3x - 24

# グラフ
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

# リスト3-3　y=3x のグラフ

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# データ
x = np.arange(-1.0, 1.01, 0.01)
y = 3 * x  # 一次関数

# グラフを描画
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

# y = x**2 のグラフ

# 二次関数
y = x**2

# グラフを描画
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

# y = x**3 - x のグラフ

# 三次関数
y = x**3 - x

# グラフを描画
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

