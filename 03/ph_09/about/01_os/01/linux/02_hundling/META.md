# metacharacters

* 通称`メタキャラクタ`
* シェルによって処理される
* 個々のコマンドがメタキャラクタを理解して処理しているわけではない
    * コマンドが実行される前に、メタキャラクタは実際のファイル名に展開される
        * `*.txt`は`a0.txt〜b5.txt`という個別のファイル名に展開された後にコマンドが実行される
        * コマンにとっては、引数に`a0.txt〜b5.txt`が指定された、と解釈している

## 概要

* `*`の利用
* `?`の利用
* `[]`の利用
* `^`の利用

## 事前準備

```bash
find ./ -name 'create_files.sh'
bash 02_hundling/create_files.sh
ls 02_hundling/metacharacter
cd 02_hundling/metacharacter
```

## 前提条件

* 02_hundling/metacharacterに移動していること
* 02_hundling/metacharacter/にファイルが生成されていること

### 実施

#### `*`の利用

* `0文字以上の任意の１文字`
    * 例: `abc*`のパターンの場合
        * abc123
        * abcdef
        * abc

```bash
#末尾が`.txt`のファイルのみ表示
ls *.txt
```

#### `?`の利用

* １文字だけを表す

```bash
ls ?.txt
#ls: ?.tst: No such file or directory
ls a?.txt
#a0.txt  a1.txt  a3.txt  a4.txt  a5.txt
```

#### `[]`の利用

* `[]`内の１文字とマッチ
    * 文字列でない点に注意

```bash
#a またはb で始まり、2文字目が3または4
ls [ab][34]*
#a3.dat  a3.txt  a4.dat  a4.txt  b3.dat  b3.txt  b4.dat  b4.txt
```

#### `^`の利用

* 列挙された文字以外を表す

```bash
# b で始まらないファイルだけを表示
ls [^b]*
#a0.dat  a0.txt  a1.dat  a1.txt  a3.dat  a3.txt  a4.dat  a4.txt  a5.dat  a5.txt
```