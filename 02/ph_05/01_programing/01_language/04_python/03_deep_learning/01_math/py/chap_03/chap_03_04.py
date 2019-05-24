# リスト3-6　垂直二等分線の式とグラフ

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# 基となる線分の傾きと切片
a1 = (5-1)/(6-0)
b1 = 1

# 線分の中点
cx = (0 + 6) / 2
cy = (1 + 5) / 2

# 線分に直交する直線の傾き(a2 = -1/a1)
a2 = -1 / a1

# 線分に直交する直線の切片(b2 = y - a2*x)
b2 = cy - a2*cx

# 直線の式
x = np.arange(0, 7)   # xの値
y1 = a1*x + b1   # もとの直線
y2 = a2*x + b2   # 垂直二等分線

# 描画
plt.plot(x, y1)
plt.plot(x, y2)
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# リスト3-7　三角比を使って円を描画

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# 角度
th = np.arange(0, 360)

# 円周上の点Pの座標
x = np.cos(np.radians(th))
y = np.sin(np.radians(th))

# 描画
plt.plot(x, y)
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# 4.4　三角比と角度

rad = np.arctan2(3, 4)  # 角度を求める（ラジアン）
th = np.degrees(rad)    # 度数法に変換
th