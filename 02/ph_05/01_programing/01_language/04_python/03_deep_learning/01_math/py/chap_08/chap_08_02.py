# リスト8-3　関数と導関数のグラフを描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# xの値
x = np.arange(-10, 10, 0.1)

# 元の関数 f(x) = x**3 + 3x**2 + 3x + 1
y = x**3 + 3*x**2 + 3*x + 1
plt.plot(x, y)
plt.grid(color='0.8')
plt.show()

# 導関数 f'(x) = 3x**2 + 6x + 3
y2 = 3*x**2 + 6*x + 3
plt.plot(x, y2)
plt.grid(color='0.8')
plt.show()