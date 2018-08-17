# 履歴の操作

## ファイルを最新のコミットに戻す

```bash
#既存ファイルに追記する
echo “reset test” >> sample.txt
#追記できていることを確認
cat sample.txt
#最新のコミットの状態に戻る ※ファイル名は指定できない
git reset —hard HEAD
```

```text
"『git reset HEAD ファイル』の場合、作業フォルダの内容はそのままで、インデックスからアンステージするが、
『git reset —hard HEAD』の場合には、作業フォルダの内容とインデックスの内容が全て破棄される。"
```

```bash
#“reset test”という追記が消えていることを確認
cat sample.txt
#もう一度、追加書き込みをする
echo “reset test” >> sample.txt
#addしてインデックスに載せる
git add .
#インデックスにファイルがあることを確認する
git status
#最新のコミット状態に戻す
git reset —hard HEAD 
#インデックスからアンステージされていることを確認する
git status
```

## 特定のファイルのみ最新コミット(HEAD)の状態に戻す

```bash
#sample.txt(既存ファイル)がある場合には削除する
rm sample.txt
#新規ファイルを作成
echo “残す” > checkout_test.txt
#新規ファイルを作成
echo “残す” > not_checkout.txt
#addしてインデックスに載せる
git add .
#コミットする(テスト用の最新コミットを作成)
git commit
#ファイルに追記する
echo “残さない” >> checkout_test.txt
#ファイルに追記する
echo “残す” >> not_checkout.txt
#コミットする
git commit -a
#checkout_test.txtを最新コミットの状態に戻す
git checkout HEAD checkout_test.txt
#“残さない”テキストが消えていることを確認
cat checkout_test.txt
#“残す”が２行残っていることを確認
cat not_checkout.txt
```

## 特定のファイルのみ復元する

```bash
#IDを確認する
git log —oneline
#sample.txt(先ほど削除したファイル)が残っているIDを指定
git checkout ID ファイル名
#復元されていることを確認する
ls
```

# 最新のコミットメッセージを修正する

```bash
#viが起動するので、メッセージを修正する
git commit -—amend
#コミットメッセージが修正され、IDが変更されていることを確認
git log
```

# １つ前のHEADに戻る

```bash
#新規ファイル追加
touch head.txt
#addしてインデックスに載せる
git add .
#コミットする
git commit -m “ここに戻る”
#ファイルに書き込みをする
echo “will delete” >> head.txt
#addしてインデックスに載せる
git commit -am “これはHEADになる”
#ログを確認する
git log —oneline
```

```text
"dc08510 (HEAD -> master) これはHEADになる
09b0b9c ここに戻る
〜以下略〜"
```

```bash
#１つ前のHEADに戻る
git reset —hard HEAD~
```

```text
HEAD is now at 09b0b9c ここに戻る
```

## ２つ前のHEADに戻る

```bash
#新規ファイル追加
touch 2head.txt
#addしてインデックスに載せる
git add .
#コミットする
git commit -m “２個前”
#ファイルに書き込みをする
echo “will delete” >> 2head.txt
#addしてインデックスに載せる
git commit -am “スキップされる”
#ファイルに書き込みをする
echo “will delete too” >> 2head.txt
#addしてインデックスに載せる
git commit -am “HEADになる”
#ログを確認する
git log —oneline
```

```text
"f6645e3 (HEAD -> master) HEADになる
fe36d4e  スキップされる
f91e234 ２個前
〜以下略〜"
```

```bash
#２個前のHEADに戻る
git reset —hard HEAD~2
#ログを確認する
git log —oneline
```

```text
HEAD is now at f91e234 ２個前
```

## インデックスからファイルを削除する(今後もコミットする予定のないファイルに対して行う)

```bash
cd ../
rm -rf local
mkdir local
cd local
git init
```

```bash
touch aa bb cc dd ee ff gg
```

```text
"untracked files:
        aa
        bb
        cc
        dd
        ee
        ff
        gg
nothing added to commit …"
```

```bash
git add .
```

```text
"changes to be committed:
        new file:    aa
        new file:    bb
        new file:    cc
        new file:    dd
        new file:    ee
        new file:    ff
        new file:    gg"
```

```bash
git status
```

```text
"changes to be committed:
        new file:    aa
        new file:    bb
        new file:    cc
        new file:    dd
        new file:    ee
        new file:    ff
        new file:    gg"
```

```bash
#インデックスからaaをアンステージする
git rm —cached aa
```

```bash
git status
```

```text
"changes to be committed:
        new file:    bb
        new file:    cc
        new file:    dd
        new file:    ee
        new file:    ff
        new file:    gg
untracked files:
        aa"
```

```bash
#作業ファイルでは消えていないことを確認
git status
#インデックスからaaとbbをアンステージする
git rm —cached bb cc
```

```bash
git status
```

```text
"changes to be committed:
        new file:    dd
        new file:    ee
        new file:    ff
        new file:    gg
untracked files:
        bb
        cc"
```

```bash
git commit -m “defg”
```

```text
"4files changed, 0insertions(+), 0deletions(-)
create mode 100644 dd
create mode 100644 ee
create mode 100644 ff
create mode 100644 gg"
```

## 最新のコミットにさらに変更を追加する

```bash
#ファイルに追記する
echo “aa” >> aa
#addしてコミットする
git commit -am “add aa”
#ログを確認する
git log —oneline
#ファイルに追記する
echo “bb” >> aa
#エディタが開くのでそのまま保存
git commit —amend
#HEADに新規に追加した変更が反映されている
git log —oneline
```

```text
"・コミットするときは常にインデックスの状態が履歴となる
・—amendなし＝HEADの指すコミットに続く履歴となる
・—amendあり＝HEADの指すコミットを修正した履歴となる"
```

## バージョン管理が無視するファイルを指定する

```bash
#新規ファイルを作成
touch ignoreFile
#.igitgnoreというファイルを作成し、無視するファイル名を記載
echo “ignoreFile” > .gitignore
#変更してみる
echo “This file will be ignored” >> ignoreFile
#addする
git add .
#変更ファイルの中にignoreFileは含まれていないことを確認
git status
```

```text
"untracked files:
        .gitignore"
```

```bash
#先ほどのファイルにさらに追記してみる
echo “ignore??” >> ignoreFile
#addする
git add .
#やはり追加されないことを確認
git status
```

```text
"on branch master
nothing to commit, working tree clean"
```

## バージョン管理が無視するファイルを途中から指定する

```bash
#新規ファイル作成
touch addedFile
#addする
git add .
#.gitignoreに無視するファイルとして登録
echo “addedFile” >> .gitignore
#ステージに変更が反映されてしまっていることを確認する
git staus
#アンステージする
git rm —cached addedFile
#アンステージされたことを確認する
git status
#ファイルに変更を与える
echo “ignore test” >> addedFile
#今度は変更が反映されていないことを確認する
git status
```