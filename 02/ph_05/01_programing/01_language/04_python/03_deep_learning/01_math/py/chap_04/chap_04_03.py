# 3.1　貢献度を計算する

import math
10 * math.cos(math.radians(60))

# リスト4-1　直線AB、CDのなす角度

import math
import numpy as np

# 座標
a = np.array([2, 7])
b = np.array([6, 1])
c = np.array([2, 3])
d = np.array([6, 5])

# ベクトルaとベクトルbの成分
va = b - a
vb = d - c

# ベクトルの大きさ
norm_a = np.linalg.norm(va)
norm_b = np.linalg.norm(vb)

# ベクトルの内積
dot_ab = np.dot(va, vb)

# 角度を求める
cos_th = dot_ab / (norm_a * norm_b)
rad = math.acos(cos_th)
deg = math.degrees(rad)
print(deg)