# 2.2　場合の数の求め方

# 集合の要素数
A = {2, 4, 6, 8, 10}
B = {3, 6, 9}
len(A | B)

# 順列

import itertools
num = {1, 2, 3, 4, 5}  # データを定義
A = set(itertools.permutations(num, 3))  # numの中から3個を選ぶ順列で集合を生成
len(A)  # Aの要素数

for a in A:
    print(a)

# 2.4　階乗

num = {1, 2, 3, 4, 5}  # データを定義
A = set(itertools.permutations(num, 5))  # numの中から5個を選ぶ順列
len(A)

import math
math.factorial(5)  # 5の階乗

# 2.5　重複順列

num = {1, 2, 3, 4, 5}  # データを定義
A = set(itertools.product(num, num, num))  # numの中から3個を選ぶ重複順列
len(A)

for a in A:
    print(a)

# 2.6　組み合わせ

num = {1, 2, 3, 4, 5}  # データを定義
A = set(itertools.combinations(num, 3))  # numの中から3個を選ぶ組み合わせ
len(A)

for a in A:
    print(a)

# 2つのサイコロを同時に振ったときの目の出方

dice = {1, 2, 3, 4, 5, 6}  # サイコロの目を定義
A = set(itertools.combinations(dice, 2))  # diceから2個を選ぶ組み合わせ
len_A =len(A)  # 組み合わせが何通りあるか
len_A+6        # 組み合わせの場合の数＋2つのサイコロの目が同じになる場合の数