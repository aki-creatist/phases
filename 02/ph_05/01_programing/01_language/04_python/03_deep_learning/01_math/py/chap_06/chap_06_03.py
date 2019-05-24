# リスト6-1　1の目が出る確率

import random

# サイコロを振る
cnt= 0  # 1が出た回数
for i in range(10000):
    dice = random.randint(1, 6)
    if dice == 1:
        cnt += 1

# 確率を求める
p = cnt / 10000
print(p)

# リスト6-2　すべての事象が起こる確率

import random

# サイコロを振る
hist = [0] * 7
for i in range(10000):
    dice = random.randint(1, 6)
    hist[dice] += 1

# 確率を求める
p = [0] * 7
for i in range(1, 7):
    p[i] = hist[i] / 10000
    print(i, p[i])

# 確率を合計
print('------------------\n' + str(sum(p)))

# 3.3　積の法則と和の法則

# 3番目にくじを引く人の確率
from fractions import Fraction
x = Fraction(2, 7) * Fraction(5, 6) * Fraction(1, 5)  #（A当たり→Bはずれ→C当たり）
y = Fraction(5, 7) * Fraction(2, 6) * Fraction(1, 5)  #（Aはずれ→B当たり→C当たり）
z = Fraction(5, 7) * Fraction(4, 6) * Fraction(2, 5)  #（Aはずれ→Bはずれ→C当たり）
p = x + y + z  # X、Y、Zのいずれかが起こる確率
p

# リスト6-3　円周率を求める

#%matplotlib inline
import matplotlib.pyplot as plt
import random
import math

# 点を描画
cnt = 0
for i in range(3000):
    x = random.randint(1, 100)
    y = random.randint(1, 100)
    d = math.sqrt((x-50)**2 + (y-50)**2) #中心と点との距離
    if (d <= 50 ):
        cnt += 1   # 円内の点を数える
        plt.scatter(x, y, marker='.', c='r')  # 赤色の点を描画
    else:
        plt.scatter(x, y, marker='.', c='g')  # 緑色の点を描画
plt.axis('equal')
plt.show()

# 円周率を求める
p = cnt / 3000  # 点が円の中にある確率
pi = p * 4      # 円周率
print(pi)
