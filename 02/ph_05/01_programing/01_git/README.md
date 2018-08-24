# Git

* [Gitの使い方](01)
* [GitHubの使い方](02)
* [クローンとプル](03)
* [コンフリクトとマージ](04)
* [履歴の操作](05)
* [リモートリポジトリで作業する](06)

## 最初にやること
    
### .DS_Storeの無視設定(Mac)

* Mac OS X環境の場合、Finderが `.DS_Store` という不可視ファイルを自動で追加する
    * これはFinderで開いたときの見え方を決める情報なので、プロジェクトとは無関係
    * あらかじめGit管理外であることを明示する

```bash
#.DS_Storeを無視するグローバル設定
git config --global core.excludesfile $HOME/.gitexclude
echo ".DS_Store" >> $HOME/..gitexclude
#.DS_Storeを無視するローカル設定
echo ".DS_Store" >> .gitignore
```

* すでにaddして.DS_Storeがインデックスにある場合
    * 実行した後に改めて、セッティング

```bash
# インデックスのファイルを削除する
git rm --cached .DS_Store
```

* Git管理から外す方法は以下の３つ
    * .gitignoreにファイル名を追記
    * info/excludeにファイル名を追記
    * info/excludeにファイル名を追記
    
```bash
# プロジェクトを共有するメンバー全員が無視するファイルを共有できるので親切
echo "ファイル名" >> プロジェクトフォルダ/.gitignore    
# プロジェクトのバージョン管理には含めずに無視をする(Macを利用する人が自分だけならこれでOK。)
echo "ファイル名" >> プロジェクトフォルダ/info/.exclude
# 全プロジェクトに効く設定
git config --global core.excludesfile $HOME/.gitexclude
echo ".DS_Store" >> $HOME/..gitexclude
```

* １と２の方法はプロジェクトごとに設定する必要がある
    * 他にも)他にもMac使用が想定できる場合には２ではなく１を選択する
* また、プロジェクトごとに設定するのは面倒
    * 同一ユーザーで操作する際には全プロジェクトで.DS_Storeを無視する設定
* 今回は１と３を併用する

## GitHub

### アカウントとリポジトリを作成する

* [アカウント作成〜リポジトリ作成](http://qiita.com/kooohei/items/361da3c9dbb6e0c7946b)

### 鍵認証する

* [鍵認証](http://monsat.hatenablog.com/entry/generating-ssh-keys-for-github)

### リモートリポジトリを一つ前に戻す

[リモートリポジトリにreset --hard head^を行う](http://tmtms.hatenablog.com/entry/20101221/git)

### htdocsをアップロード

* htdocsをアップロードする際には、以下のファイルを.gitignoreに追記
    * htdocs/.gitignore

```text
applications.html
dashboard
img
webalizer
bitnami.css
favicon.ico
```

## 基本

```bash
# Gitのインストール
yum install git
```

### # Gitに管理する場所を教える

```bash
# フォルダの作成と移動
mkdir demo
cd demo
# このフォルダをGitで管理することを宣言する
git init
```

### 変更を記録する

```bash
# sample.txtに書き込み、表示
echo "ただいまテスト中" > sample.txt
cat sample.txt
# sample.txtを変更したことをGitに伝える
git add sample.txt
# 変更を記録するようにGitに依頼する 
git commit -m "はじめの一歩" #-mオプションに続くものは、歴史を記録した時のメッセージとして保存される
# ファイルの中身を修正
echo "ただいまGitのテスト中。" > sample.txt
cat sample.txt
# Gitに変更を伝える
git add sample.txt
# 変更を記録する
git commit -m "句読点を追加"
# 1行追加する
echo "Gitは簡単！" >> sample.txt
cat sample.txt
# 変更を伝える
git add sample.txt
# 変更を記録する
git commit -m "一行追加"
```

### 変化を知る

```bash
# 履歴の表示
git log
# 一行に収めて表示
git log --oneline
# 変化を表示
git diff 比較ファイル 比較ファイル
```

### 過去を復元する

* Gitが管理するフォルダにおいては、ファイルは絶対的なものではない
* データを一時的に置いておく作業領域でしかない
* ファイルの内容の変化の歴史はGitに保存されている
* ファイルは、ユーザーとGitの間を取り持つ媒体

```bash
# ファイルの削除
rm sample.txt
cat sample
# コミットIDを確認する
git log --oneline
# 復元する
git checkout コミットID sample.txt
cat sample.txt
# 好きな過去に戻る
git checkout コミットID sample.txt
# 好きな過去に戻る２
git checkout コミットID sample.txt
```

### 先にファイルを作成する

```bash
# 先にファイルを作成する
mkdir board
echo "&lt;?php" > board.php
cat board.php
# エラーを起こす
git add board.php
```

* フォルダに対してgit initするよりも前に、git addを行うと下記のエラーとなる

```bash
fatal: Not a git repository #(致命的：gitリポジトリ.gitが存在しない)
```

```bash
# 改めてgit init
git init
git commit
echo "vimを起動する" > sample.txt
cat sample.txt
git add sample.txt
git init
git add sample.txt
git commit
git config --global user.name "名前"
git config --global email xxx@example.com
git commit --amend --reset-author
git log
git rev-parse HEAD
git log
```

### プロジェクトを始める

```bash
rm .git/info/exclude
mkdir project
cd project
git init
echo "<?php" > sample.txt
git add .
git commit -m "PHP開始タグを書き込み"
git commit -a -m "PHP終了タグを追加"
echo "?>" >> sample.txt
git show
git reset --hard HEAD sample.txt
git commit --amend
# ファイル名を変更
mv sample.txt if.php
# ファイル名を変更を知らせる
git add .
git commit -m "ファイル名の変更"
# 差分を確認する
git diff
```

#### ファイル名変更前の状態

| リポジトリ | インデックス | 作業フォルダ |
|:----|:----|:----|
| (HEAD)  "PHP開始タグを追加" | sample.txt | sample.txt |

#### ファイル名を変更したところ

| リポジトリ | インデックス | 作業フォルダ |
|:----|:----|:----|
| (HEAD)  "PHP開始タグを追加" | sample.txt | sample.php |

#### git add . したところ

| リポジトリ | インデックス | 作業フォルダ |
|:----|:----|:----|
| (HEAD)  "PHP開始タグを追加" | sample.txt<br>sample.php | sample.php |

つまりgit add . はインデックスにファイルを追加したり、変更を保存不可

```bash
git rm sample.txt
git commit --ammend
# ファイル名を変更する
git mv if.php rename.php
git commit -m 'ファイル名変更テスト1'
```
