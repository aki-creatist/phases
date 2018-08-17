# 基本

## ファイルの変更履歴の保存と復元

```bash
#フォルダへ移動
cd /c/xampp/htdocs		
#カレントディレクトへのパスを確認する
pwd
#任意のディレクトリ名	作業フォルダの作成	
mkdir
#リポジトリ(変更記録の貯蓄場所)の初期化
git init
#ファイル作成+書き込み
echo “1st commit” > 新ファイル	
#ファイルを表示
cat ファイル名	
#ファイルを表示
git add ファイル名	
#インデックス(=変更内容の一時保存場所の内容をリポジトリにコピー
git commit -m “メッセ"
```

```bash
#履歴の確認
git log
#ファイルに追加書き
echo “2nd commit” >> ファイル	
#差分の確認
git diff 旧ID 新ID
#ファイルを削除する
rm ファイル
#失ったファイルを復元する
git checkout ID ファイル名
```

## 様々な書き方(ディレクトリ内を全てaddする)

```bash
#最新コミットのIDを確認
git rev-parse HEAD
#追加書き
echo “3rd commit” >> ファイル
#カレントディレクトリ内を全てaddする
git add .
#コミットする
git commit -m “3rd commit” >> ファイル
#履歴を確認する
git log
#履歴を確認する
git show
```

## 様々な書き方(addからcommitまで一括で行う)	

```bash
#追加書き
echo “4th commit” >> ファイル
#addからcommitまで一括処理( -am とも書ける)
git commit -a -m “4th commit”
```

## 一括で行うオプションの注意

```bash
#新規ファイル作成
echo “will mistake” > 新ファイル
#警告が出る
git commit -a -m “will mistake”
```

```text
"「追加のコミットはありませんが追跡されていないファイルがあります」
という内容のメッセージが表示される
「追跡するにはgit addしましょう」という意味"

"HEAD detached from 568a4fa
untracked files:
    新ファイル
nothing added to commit but untracked files present"
```

-aでaddからcommitまで一括で行えるのはインデックスに置かれたことのあるファイルだけ

```bash
#リポジトリにコピーされていないことを確認する
git log (もしくは(git show)
```

## 既存ファイルと合わせて行う場合には可能

```bash
#ファイル変更
echo “5th commit” >> 既存ファイル
#変更された既存ファイルと一緒に行う場合にはaddからcommitの一括処理ができてしまう
git commit -am “新規と既存を一緒にコミット”
```

## 間違ってインデックスに載せたファイルを削除する

* コミットしたくないファイルをgit add . でディレクトリごとaddしてしまったときの対処)

```bash
#既存ファイルに追加書きをしてファイルを変更する
echo “6th commit” >> 既存ファイル
#新規ファイルを作成
echo “will deleted” > 新規ファイル
#インデックスに登録
git add .
#引数を付けずにコミットする
git commit
```

```text
"# changes to be committed:
#          new file:    新規ファイル　←このファイルはコミットしたくない
#          modified:  既存ファイル"
```

```bash
#コミットしたくないファイルをアンステージ(インデックスから下ろす)する
git reset HEAD
"git commit -a
#確認後viを:qで抜ける"

#不要になったファイル削除
rm 新規ファイル
#必要なものだけ改めてコミット
git commit -m “メッセ”
```
