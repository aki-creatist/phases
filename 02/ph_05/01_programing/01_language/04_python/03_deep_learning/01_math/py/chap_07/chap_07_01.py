# リスト7-1　CSVファイルの読み込み

import pandas as pd

# score.csv の読み込み
dat = pd.read_csv('score.csv', encoding='SHIFT-JIS')
dat.head()

# リスト7-2　平均値、中央値、最頻値を求める

import pandas as pd
import numpy as np

# score.csvの読み込み
dat = pd.read_csv('score.csv', encoding='SHIFT-JIS')

# 平均値、中央値
print('平均値', np.mean(dat['数学']))
print('中央値', np.median(dat['数学']))

# 最頻値
bincnt = np.bincount(dat['数学'])  # 同じ値の個数を数える
mode = np.argmax(bincnt)  # bincntの中で最も大きな値を取得
print('最頻値', mode)

# リスト7-3　度数分布図を描画する

#%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd

# score.csv の読み込み
dat = pd.read_csv('score.csv', encoding='SHIFT-JIS')

# 各階級に含まれる度数を数える
hist = [0]*10 # 度数（要素数10、0で初期化）
for dat in dat['数学']:
    if dat < 10:   hist[0] += 1
    elif dat < 20:  hist[1] += 1
    elif dat < 30:  hist[2] += 1
    elif dat < 40:  hist[3] += 1
    elif dat < 50:  hist[4] += 1
    elif dat < 60:  hist[5] += 1
    elif dat < 70:  hist[6] += 1
    elif dat < 80:  hist[7] += 1
    elif dat < 90:  hist[8] += 1
    elif dat <= 100:  hist[9] += 1
print('度数:', hist)

# 度数分布図
x = list(range(1,11))  # x軸の値
labels = ['0~','10~','20~','30~','40~','50~','60~','70~','80~','90~']  # x軸の目盛りラベル
plt.bar(x, hist, tick_label=labels, width=1)# 棒グラフを描画
plt.show()