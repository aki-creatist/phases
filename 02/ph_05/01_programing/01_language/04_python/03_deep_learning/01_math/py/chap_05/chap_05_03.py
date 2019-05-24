# 3.1　ベクトルと行列の関係

import numpy as np
p = np.matrix([[3], [2]])        # 点Pの座標
A = np.matrix([[2, 0], [1, 2]])  # 変換行列A
A * p

# リスト5-1　x軸に対して線対称に移動

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 三角形ABCの頂点
p = np.matrix([[1, 3, 3, 1], [1, 1, 2, 1]])

# 変換行列（x軸に線対称）
A = np.matrix([[1, 0], [0, -1]])

# 変換
p2 = A * p
print(p2)

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# y軸に線対称

p = np.matrix([[1, 3, 3], [1, 1, 2]])  # 三角形ABCの頂点
A = np.matrix([[-1, 0], [0, 1]])       # 変換行列A（y軸に線対称）
A * p

# 座標原点に点対称

p = np.matrix([[1, 3, 3], [1, 1, 2]])  # 三角形ABCの頂点
A = np.matrix([[-1, 0], [0, -1]])      # 変換行列A（原点に点対称）
A * p

# 直線y=x に線対称

p = ([[1, 3, 3], [-1, -1, 0]])  # 三角形ABCの頂点
A = np.matrix([[0, 1], [1, 0]]) # 変換行列A（直線y=xに線対称）
A * p

# リスト5-2　図形の相似拡大

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 三角形ABCの頂点
p = np.matrix([[1, 1, 2, 1], [3, 1, 1, 3]])

# 変換行列（3倍に拡大）
A = np.matrix([[3, 0], [0, 3]])

# 変換
p2 = A * p
print(p2)

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# リスト5-3　図形の回転

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 四角形ABCDの頂点
p = np.matrix([[3, 3, 5, 5, 3], [3, 1, 1, 3, 3]])

# 変換行列（反時計まわりに45度回転）
th = np.radians(45)     # 度数法 -> 弧度法
A = np.matrix([[np.cos(th), np.sin(-th)], [np.sin(th), np.cos(th)]])

# 変換
p2 = A * p
print(p2)

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# リスト5-4　図形の平行移動

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 三角形ABCの頂点（同次座標）
p = np.matrix([[1, 3, 3, 1], [1, 1, 2, 1],[1, 1, 1, 1]])

# 変換行列（平行移動）
A = np.matrix([[1, 0, 2], [0, 1, 3], [0, 0, 1]])

# 変換
p2 = A * p
print(p2)

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# リスト5-5　一次変換の組み合わせ（平行移動→回転）

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 三角形ABCの頂点（同次座標）
p = np.matrix([[1, 3, 3, 1], [1, 1, 2, 1],[1, 1, 1, 1]])

# 変換行列
A = np.matrix([[1, 0, 2], [0, 1, 3], [0, 0, 1]])  # 平行移動
th = np.radians(90)
B = np.matrix([[np.cos(th), np.sin(-th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])  # 回転行列

# 変換
p2 = B * A * p  # 平行移動->回転
print(p2)

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# 回転→平行移動

#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 三角形ABCの頂点（同次座標）
p = np.matrix([[1, 3, 3, 1], [1, 1, 2, 1],[1, 1, 1, 1]])

# 変換行列
A = np.matrix([[1, 0, 2], [0, 1, 3], [0, 0, 1]])  # 平行移動
th = np.radians(90)
B = np.matrix([[np.cos(th), np.sin(-th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])  # 回転行列

# 変換
p2 = A * B * p  # 回転->平行移動
print(p2.astype(np.int64))

# 描画
p = np.array(p)
p2 = np.array(p2)
plt.plot(p[0, :], p[1, :])
plt.plot(p2[0, :], p2[1, :])
plt.axis('equal')
plt.grid(color='0.8')
plt.show()