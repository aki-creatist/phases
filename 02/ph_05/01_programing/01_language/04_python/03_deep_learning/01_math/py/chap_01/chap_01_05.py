# リスト1-4　10進数から2進数に変換する（実数対応版）

def dec2bin_ex(target):
    # targetを整数部と小数部に分ける
    i = int(target)  # 整数部
    f = target - i  # 小数部

    # 整数部を2進数に変換
    a = []  # 余りを入れるリスト

    # 割り算の商が0になるまで
    while i != 0:
        a.append(i % 2)  # 余り
        i = i // 2  # 商

    # 要素を逆順にする
    a.reverse()

    # 小数部を2進数に変換
    b = []  # 整数部を入れるリスト
    n = 0  # 繰り返した回数

    # 2を掛けた後の小数部が0になるまで
    while (f != 0):
        temp = f * 2  # 小数部×2
        b.append(int(temp))  # 整数部
        f = temp - int(temp)  # 小数部
        n += 1
        if (n >= 10):
            break

    # 2進数に変換した値
    return a, b

dec2bin_ex(10.625)