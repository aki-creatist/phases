# 2.1　直線の表し方

from sympy import Symbol, solve
a = Symbol('a')   # 文字の定義
b = Symbol('b')
ex1 = -1*a + b - 2  # -a + b - 2 = 0
ex2 = 2*a + b - 4   # 2*a + b - 4 = 0
solve((ex1, ex2))   # 連立方程式を解く

# 2.2　2直線の交点

from sympy import Symbol, solve
k = Symbol('k')  # 文字の定義
t = Symbol('t')
ex1 = 4*k - 4*t      # 4*k - 4*t = 0
ex2 = -6*k -2*t + 4  # -6*k - 2*t + 4
solve((ex1, ex2))     # 連立方程式を解く