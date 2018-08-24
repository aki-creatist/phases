# 個人開発演習の準備

## 講師

* 講師はローカルで受講生全員分のディレクトリを作成
* 受講生の共有ディレクトリをクローンする
* ローカルから各々の共有ディレクトリを追跡する

## 受講生

* リモートディレクトリを作成する
* 個人開発演習の作業内容をプッシュする
* 随時コミットする

```bash
mkdir ~/Desktop/remote.git
cd remote.git
git init —bare —shared
#GUIから共有設定を行う
```

### GUIから共有設定を行う

* remote.gitをエクスプローラで右クリック
* 共有タブを開く
* 共有(S)..をクリック
* ブルダウンメニューを開きEveryoneを指定する
* 追加(A)をクリック
* 右下の、共有(H)をクリック

## 講師

* 受講生のベアリポジトリをクローン

```bash
cd 作業フォルダ
git push ~/Desktop/remote.git master
#cloneする
composer update
git branch -a
git branch constants origin/master
```
