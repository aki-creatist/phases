# リスト8-4　棒の太さを変えて面積を求める

def calc_area(dx):
    h = 0     # 棒の高さ
    area = 0  # 面積
    cnt = int(10 / dx)  # 棒の数
    for i in range(1, cnt+1):
        h = i * dx     # 高さ
        s = h * dx     # 棒の面積
        area += s      # 面積を合計
    return area

calc_area(1)

# 3.5　積分の公式

# f(x) = x**2 + 2x + 5 の不定積分
def F(x):
    return 1/3*x**3 + x**2 + 5*x

a = F(-3)  # F(a)
b = F(3)   # F(b)
b-a        # F(b)-F(a)

# SciPy.integrate.quad()関数

from scipy import integrate

# f(x) = x**2 + 2x + 5
def func(x):
    return x**2 + 2*x + 5

integrate.quad(func, -3, 3)