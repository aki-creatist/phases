# 4.1　法線ベクトル

import numpy as np
a = np.array([0, 1, 2])  # ベクトルaの成分
b = np.array([2, 0, 0])  # ベクトルbの成分
np.cross(a, b)           # 外積

# 4.2 面積を求める

a = np.array([2, 4])  # ベクトルaの成分
b = np.array([3, 1])  # ベクトルbの成分
cross_ab = np.cross(a, b)     # 外積を求める
s = np.linalg.norm(cross_ab)  # ベクトルの大きさを求める（平行四辺形の面積）
s / 2   # 三角形の面積