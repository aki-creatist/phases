# リスト8-5　接線を描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# xの値
x = np.arange(-1, 1, 0.1)

# 基の関数
y = 2*x*x + 3

# 接線
a = 4*0.25            # 導関数 f'(x)= 4x（傾き）
b = 3.125 - a * 0.25  # 切片 b = y - ax
y2 = a*x + b          # 接線の式

# グラフを描画
plt.plot(x, y)   # 基の関数
plt.plot(x, y2)  # 接線
plt.grid(color='0.8')
plt.show()

# リスト8-6　画像の輪郭を抽出する

#% matplotlib
inline
import matplotlib.pyplot as plt
from PIL import Image

# 画像読み込み
src_img = Image.open('sample.png')
plt.imshow(src_img)
plt.show()

# 画像サイズ
width, height = src_img.size

# 出力用
dst_img = Image.new('RGB', (width, height))

# カラー -> モノクロ
src_img = src_img.convert("L")

# 輪郭抽出
for y in range(0, height - 1):
    for x in range(0, width - 1):
        # 明るさの差を調べる
        diff_x = src_img.getpixel((x + 1, y)) - src_img.getpixel((x, y))
        diff_y = src_img.getpixel((x, y + 1)) - src_img.getpixel((x, y))
        diff = diff_x + diff_y

        # 出力
        if diff >= 20:
            dst_img.putpixel((x, y), (255, 255, 255))
        else:
            dst_img.putpixel((x, y), (0, 0, 0))
plt.imshow(dst_img)
plt.show()

# リスト8-7　トイレットペーパーの長さを求める

from scipy import integrate
import math

# 半径rの円の円周を求める
def calc_area(r):
    return 2 * math.pi * r

# 半径2～5の区間の円周の合計
s = integrate.quad(calc_area, 2, 5)
print(s)

# トイレットペーパーの長さ
x = s[0] / 0.011
print(x)

# 4.5　球の体積と表面積

import math

# テニスボールの半径
r = 3.4

# 体積
v = 4/3 * math.pi * r**3
v

# 表面積
s = 4 * math.pi * r**2
s