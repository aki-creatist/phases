# 1.3　ベクトルの方向

import math
rad = math.atan2(3, 2)  # 角度を求める（ラジアン）
th = math.degrees(rad)  # 度数法に変換
th

# 1.5　ベクトルの演算

import numpy as np
a = np.array([2, 2])  # ベクトルaの成分
b = np.array([2, -1]) # ベクトルbの成分

# 足し算
a + b

# 引き算
a - b

# 実数倍
2 * a