# ブランチ

## 履歴を分岐させ、統合する

```bash
mkdir local
git init
echo "master01" > sample.txt
git add .
git commit -m "master01"
```

```bash
#ログを確認する
git log —oneline
#現在作業しているブランチを確認する
git branch
#developというブランチを作成する
git branch develop
```

### master

```bash
#ブランチが切れたかどうか確認する
git branch
#ブランチを切り替える
git checkout develop
```

### develop

```bash
#ブランチを切り替えられたか確認する
git branch
#sample.txtに追記する
echo 'develop01' >> sample.txt
#コミット
git commit -am 'develop01'
#masterブランチに移動する
git checkout master
```

### master

```bash
#develop01が反映されていないことを確認する
git log --oneline
#developをマージする
git merge develop
#ログを確認する
git log --oneline
```

## ツリー状で表示する設定をする

```bash
git config —global alias.tree ‘log —graph —all —format="%x09%C(cyan bold)%an%Creset%x09%C(yellow)%h%Creset %C(magenta reverse)%d%Creset%s"'
```

* `%x09`: タブ区切り(タブの16進数コード0x09)
* `%an`: 修正した人(author name)
* `%h`: コミットID (hash値)
* `%d`: HEADとブランチの表示(decorate)
* `%s`: コミットメッセージの１行目(subject)
* `%C(xxx)`: 色・属性のフォーマットxxxを指定する
    * normal、black、red、green、yellow、blue、magenta、cyan、white
* `%Creset`: 色・属性のフォーマットを解除する
    * bold(太字)、dim(減光)、ul(下線)、blink(点滅)、reverse(反転)