# 1.3 実数誤差を減らす工夫

# 0.1を10回足す
a = 0
for i in range(10):
    a += 0.1
a

# 実数を使わずに計算する
a = 0
b = 0.1 * 10
for i in range(10):
    a += b

a = a / 10
a