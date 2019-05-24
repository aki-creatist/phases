# 6.1　点から直線までの距離

import math
x = 1
y = 6
a = 3
b = -4
c = -4
math.fabs(a*x + b*y + c) / math.sqrt(a**2 + b**2)  # 点と直線の距離の公式

# 6.2　直線で囲まれた領域の面積

import math
x = [1, 3, 6]   # x座標（A、B、Cの順）
y = [5, 1, 4]   # y座標（A、B、Cの順）

a = math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)  # 辺ABの長さ
b = math.sqrt((x[2]-x[1])**2 + (y[2]-y[1])**2)  # 辺BCの長さ
c = math.sqrt((x[2]-x[0])**2 + (y[2]-y[0])**2)  # 辺ACの長さ

s = (a+b+c) / 2
math.sqrt(s * (s-a) * (s-b) * (s-c))  # ヘロンの公式