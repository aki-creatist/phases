# 3.1 2点を結ぶ直線

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# データ
x = np.arange(1, 5.1, 0.1)
y = 1/2*x + (1/2)

# グラフを描画
plt.scatter(x, y)
plt.grid(color='0.8')
plt.show()

# リスト3-4　連立方程式を解く

from sympy import Symbol, solve

# 式を定義
a = Symbol('a')
b = Symbol('b')
ex1 = a + b - 1
ex2 = 5*a + b - 3

# 連立方程式を解く
print(solve((ex1, ex2)))

# リスト3-5　y=1/2x+1/2 と y=-2x+7 のグラフ

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-1, 6) # xの値
y = 1/2 * x + 1/2    # 直線1
y2 = -2 * x + 7      # 直線1に直行する直線

# グラフを描画
plt.plot(x, y)
plt.plot(x, y2)
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# 3.3　2直線の交点

from sympy import Symbol, solve

x = Symbol('x')  # 文字の定義
y = Symbol('y')

ex1 = -3/2*x + 6 - y  # 直線1の式
ex2 = 1/2*x + 2 - y   # 直線2の式

print(solve((ex1, ex2)))  # 連立方程式を解く