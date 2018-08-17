# リダイレクト

* ログの管理に役立つ
    * コマンドの正常な処理結果からエラーメッセージを除外
    * エラーメッセージのみを集める

```bash
touch known
ls known unkwon > ls.log 2> error.log
cat ls.log
#known
cat error.log
#ls: unkwon: No such file or directory
```

## 標準入力と標準出力

* １つの入り口と２つの出口
    * 入り口: データの入力元
        * `標準入力`
    * 出口: データの出力先
        * `標準出力`
        * `標準エラー出力`
* ３つ合わせて標準入出力
* 別名
    * `標準入力` - stdin (standard in)
    * `標準出力` - stdout (standart out)
    * `標準エラー出力` - stderr (standart error)

![redirect](./image/redirect.png)

* デフォルトの標準入力はキーボード
* デフォルトの標準出力と標準エラー出力は端末画面
    * 標準出力と標準エラー出力の２つがある理由
        * コマンドを実行結果と、エラーメッセージを分けて出力したい場合に便利だから

## 標準出力を任意のファイルにリダイレクトする

* リダイレクト
    * 入力元をキーボードからファイルへと切り替え
    * 出力を端末画面からファイルに切り替え
* コマンドの実行結果をファイルに記録できる
* コマンドの最後に実行結果を保存したいファイル名を指定
    * `> ファイル名` 
* 画面上には何も表示されない
    * リダイレクトによってコマンドが出力するデータはすべてファイルに向けらるたため
* 既存ファイルにはリダイレクトによる出力内容ですべて上書きされる

```bash
コマンド > ファイル
```

```bash
cat > test.txt
aaa #Enter
bbb #Enter
# Ctrl+d で終了
cat test.txt # 結果の確認
aaa
bbb
```

```bash
cal > cal.txt # calの実行結果をcal.txtに保存
cat cal.txt   # 確認
# 実行結果
   February 2018      
Su Mo Tu We Th Fr Sa  
             1  2  3  
 4  5  6  7  8  9 10  
11 12 13 14 15 16 17  
18 19 20 21 22 23 24  
25 26 27 28       
```

## 追記リダイレクト

* `>>` を使用する
    * 既存ファイルに追記ができる

```bash
コマンド >> ファイル
```

```bash
cat >> test.txt # 追記
cc #Enter
dd #Enter
cat test.txt # 追記できたことを確認
aa
bb
cc
dd
```

```bash
date >> date.txt
date >> date.txt
cat date.txt #確認
Sat Feb 17 11:34:08 JST 2018
Sat Feb 17 11:34:09 JST 2018
```

## エラーを出力するリダイレクト

* `2>`
    * `2`と`>`の間には空白なし

### 準備

* `ls` コマンドでエラーを発生させる
    * 指定したファイルが存在しないとエラーになる
    * 存在しないはずのファイル名を指定する
    
```bash
ls unknown #存在しないファイルを指定
ls: unknown: No such file or directory
```

```bash
ls unknown 2> error.log #エラーメッセージは表示されずに、error.logファイルに記録される
cat error.log 
ls: unknown: No such file or directory
```

