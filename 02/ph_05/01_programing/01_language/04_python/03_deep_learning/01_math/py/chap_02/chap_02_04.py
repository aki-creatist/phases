# リスト2-2　キャンディを持っているかどうかを判定する

def check_candy(item):
    if (item & 0b1000) != 0:   # キャンディフラグが立っているかどうか
        print('持っている')
    else:
        print('持っていない')

taro_item = 9
check_candy(taro_item)

# リスト2-3　テストの点数で成績を判定する

def func_and(score):
    if score >= 80:                        # socore が 80以上
        rank = 'A'
    elif (score >= 60) and (score < 80):  # score が 60～79 の範囲内
        rank = 'B'
    elif (score >= 40) and (score < 60):  # score が 40～59 の範囲内
        rank = 'C'
    else:                                  # 上記以外（score が 40未満）
        rank = '追試'
    return rank

rank = func_and(78)
rank

# リスト2-4　Yまたはyが入力されたかどうかを調べる

def func_or():
    a = input('犬は好きですか？（Y/N）... ')   # キー入力を促すメッセージを表示
    if (a == 'Y') or (a == 'y'):  # 「Y」または「y」が入力されたとき
        print('はい')
    else:                         # 上記以外が入力されたとき
        print('いいえ')

func_or()