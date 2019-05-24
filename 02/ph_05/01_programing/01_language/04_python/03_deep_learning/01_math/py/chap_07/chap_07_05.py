# 5.1　乱数

import random
rand = []
for i in range(10):
    rand.append(random.randint(0,100)) # 1～100までの乱数を生成
rand

# 5.2　乱数を使うときに注意すること

a = 4     # 乱数の初期値
b = 7
c = 9
rn = 1
rand = []
for i in range(20):
    rn = ((a * rn + b) % c)    # 乱数を生成
    rand.append(rn)
rand