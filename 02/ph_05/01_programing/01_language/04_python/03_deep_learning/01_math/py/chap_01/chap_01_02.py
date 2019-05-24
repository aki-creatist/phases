# リスト1-1　10進数から2進数に変換する

def dec2bin(target):
    amari = []   # 余りを入れるリスト

    # 割り算の商が0になるまで
    while target != 0:
        amari.append(target % 2) # 余り
        target = target // 2     # 商

    # リストの要素を逆順にして返す
    amari.reverse()
    return amari

dec2bin(26)

# リスト1-2 10進数から16進数に変換する

def dec2hex(target):
    amari = []  # 余りを入れるリスト

    # 割り算の商が0になるまで
    while target != 0:
        amari.append(target % 16)  # 余り
        target = target // 16  # 商

    # 余りの10～15をA～Fに置換
    for i in range(len(amari)):
        if amari[i] == 10:
            amari[i] = 'A'
        elif amari[i] == 11:
            amari[i] = 'B'
        elif amari[i] == 12:
            amari[i] = 'C'
        elif amari[i] == 13:
            amari[i] = 'D'
        elif amari[i] == 14:
            amari[i] = 'E'
        elif amari[i] == 15:
            amari[i] = 'F'

    # リストの要素を逆順にして返す
    amari.reverse()
    return amari

dec2hex(26)

# リスト1-3 m進数から10進数に変換する

def any2dec(target, m):
    n = len(target) - 1  # 指数の最大値
    sum = 0  # 10進数に変換した値

    # 文字数分の繰り返し
    for i in range(len(target)):
        if target[i] == 'A':
            num = 10
        elif target[i] == 'B':
            num = 11
        elif target[i] == 'C':
            num = 12
        elif target[i] == 'D':
            num = 13
        elif target[i] == 'E':
            num = 14
        elif target[i] == 'F':
            num = 15
        else:
            num = int(target[i])

        sum += (m ** n) * num  # 「mのn乗×各桁の値」を合計
        n -= 1  # 重みを1つ減らす
    return sum

any2dec('11010', 2)

any2dec('1A', 16)