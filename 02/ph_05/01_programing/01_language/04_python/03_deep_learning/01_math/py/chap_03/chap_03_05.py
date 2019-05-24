# リスト3-8　半径300の円を描画（y >= 0

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# 円の方程式
r = 300  # 半径
x = np.arange(-r, r+1)    # x: -300～300
y = np.sqrt(r**2 - x**2)  # y

# 描画
plt.plot(x, y)
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

# リスト3-9　中心が（200, 300）の円を描画

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# 円の中心
a = 200
b = 300

# 円の方程式
r = 300   # 半径
x = np.arange(a-r, a+r+1)          # xの値
y = np.sqrt(r**2 - (x-a)**2) + b  # y: 円の上側
y2 = -y + 2*b                      # y2: 円の下側

# 描画
plt.plot(x, y)
plt.plot(x, y2)
plt.axis('equal')
plt.grid(color='0.8')
plt.show()

