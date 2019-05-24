# リスト2-1　色情報をr、g、bに分解する

def get_pixel_color(c):
    r = (c & 0x00FF0000) >> 16 # 赤
    g = (c & 0x0000FF00) >> 8  # 緑
    b = (c & 0x000000FF)       # 青
    return r, g, b

c = 4287090426  # 色情報（10進数）
r, g, b = get_pixel_color(c) # get_pixel_color()関数を実行
print(r, g, b)

# 3.8　ビットをフラグとして利用する

# フラグの初期化
taro_item = 0
taro_item

# フラグを立てる（金貨をゲット）
taro_item = taro_item | 0b0001
taro_item

# フラグを立てる（キャンディをゲット）
taro_item = taro_item | 0b1000
taro_item

# フラグを使って判定する（キャンディを持っているかどうか）
chk_candy = taro_item & 0b1000
chk_candy

# フラグの解除（キャンディフラグをおろす）
taro_item = taro_item & (~0b1000)
taro_item

# 10進数の値を使ってフラグを立てる（宝石をゲット）
taro_item = taro_item | 4
taro_item