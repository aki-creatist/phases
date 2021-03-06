# 数学

## 位取り記数法

### 1.1 10進位取り記数法

* 10進数のこと
* 1234の場合、`(1000*1)+(100*2)+(10*3)+(1*4)`
    * 1000,100,10,1は**重み**と呼ばれる
* 重みは `基数のn乗` になる
    * `(10**3*1)+(100**2*2)+(10**1*3)+(1**0*4)`
        * 全ての重みが `10のn乗` になっている
        * 2進数なら `2のn乗` / 16進数なら `16のn乗`
* 基数は**底**とも呼ぶ

### 1.2 mの0乗

```python
10**3 #1000
10**0 #1
2**1  #1
```

### 1.3 2進位取り記数法

* 0と1の2つの数字を使う
* 並べた数字の桁は右から順に`2**0,2**1,2**2...`を表す

```python
bin(10) #10進数の10を引数として2進数に変換
#'0b1010'
```

### 1.4 16進位取り記数法

| 10進法 | 2進法 | 16進法 |
|:----:|:----:|:----:|
| 0  | 0     | 0 |
| 1  | 1     | 1 |
| 2  | 10    | 2 |
| 3  | 11    | 3 |
| 4  | 100   | 4 |
| 5  | 101   | 5 |
| 6  | 110   | 6 |
| 7  | 111   | 7 |
| 8  | 1000  | 8 |
| 9  | 1001  | 9 |
| 10 | 1010  | A |
| 11 | 1011  | B |
| 12 | 1100  | C |
| 13 | 1101  | D |
| 14 | 1110  | E |
| 15 | 1111  | F |
| 16 | 10000 | 10 |
| 17 | 10001 | 11 |
| 18 | 10010 | 12 |
| 19 | 10011 | 13 |
| 20 | 10100 | 14 |
| 21 | 10101 | 15 |
| 22 | 10110 | 16 |
| 23 | 10111 | 17 |
| 24 | 11000 | 18 |
| 25 | 11001 | 19 |
| 26 | 11010 | 1A |
| 27 | 11011 | 1B |
| 28 | 11100 | 1C |
| 29 | 11101 | 1D |
| 30 | 11110 | 1E |
| 31 | 11111 | 1F |

```python
## 10進数、2進数から16進数へ
hex(28) #10進数の28を16進数に変換
#'0x1c'
hex(0b11010) #2進数の11010を16進数に変換
#'0x1a'
```

## 基数変換

### 2.1 10進数から2進数へ

```python
def dec2bin(target):
    amari = [] # 余りを入れるリスト
    # 割り算の商が0になるまで
    while target != 0:
        amari.append(target % 2) #余り
        target = target // 2 #商
    # リストの要素を逆順にして返す
    amari.reverse()
    return amari
    
dec2bin(26) #[1, 1, 0, 1, 0]
```

### 2.2 10進数を16進数に

```python
def dec2hex(target):
    amari = [] # 余りを入れるリスト
    # 割り算の商が0になるまで
    while target != 0:
        amari.append(target % 16) # 余り
        target = target // 16           #  商
        
    # 余りの10〜15をA〜Fに置換
    for i in range(len(amari)):
        if amari[i] == 10:   amari[i] = 'A'
        elif amari[i] == 11: amari[i] = 'B'
        elif amari[i] == 12: amari[i] = 'C'
        elif amari[i] == 13: amari[i] = 'D'
        elif amari[i] == 14: amari[i] = 'E'
        elif amari[i] == 15: amari[i] = 'F'
    
    # リストの要素を逆順にして返す
    amari.reverse()
    return amari

dec2hex(26) # [1, 'A']
hex(26)     # '0x1a'
```

```python
#int()は他の位取り記数法から10進法へ変換可能
int('0b11010', 2) #26
int('0x1A', 16)   #26
```

```python
def any2dec(target, m):
    n = len(target)-1 # 指数の最大値
    sum = 0           # 10進数に変換した値
    
    # 文字数分の繰り返し
    for i in range(len(target)):
        if target[i] == 'A':     num = 10
        elif target[i] == 'B':   num = 11
        elif target[i] == 'C':   num = 12
        elif target[i] == 'D':   num = 13
        elif target[i] == 'E':   num = 14
        elif target[i] == 'F':   num = 15
        else:                    num = int(target[i])
            
        sum += (m ** n) * num  # 「mのn乗×各桁の値」を合計
        n -= 1  # 重みを1つ減らす
    return sum
```

```python
any2dec('11010', 2) # 26
```

## コンピュータの世界の数字

### データの扱い方

* バイト: データを入れる決まった大きさの入れ物の単位
* 桁あふれ/オーバーフロー:
    * 1バイトに`11111111` 入っていると仮定
    * 1を追加すると `100000000` になる状態
* 0で埋めるのは `その桁に値が何もないこと` を表すため

```python
a = 6 # 00000110が代入される
```

[tex:a\^n]