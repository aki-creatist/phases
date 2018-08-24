# 履歴の操作

## 過去のコミットを修正する

```bash
git branch rebaseEdit #ブランチ作成
git branch
git checkout rebaseEdit #移動
git branch 
```

```bash
git log —oneline
```

```text
f56574b(HEAD) add Fx CC()
2501611 add Fx BB()
795341c add Fx AA()
```

* 編集したいコミットの１つ前を指定する
* add Fx BB()を編集したいので、add Fx AA()のIDを指定する

```bash
git rebase -i 795341c
```

* エディタが起動する

```text
pick 2501611 add Fx BB()
pick f56574b add Fx CC()
```

* add Fx BB()のpickをeに書き換える

```text
e 2501611 add Fx BB()
pick f56574b add Fx CC()
```

* 以下のメッセージが表示される
    * ①…git rebaseはadd Fx BB()で停止しています。
    * ②…今、コミットは、git commit —amendで修正できます。
    * ③…変更できたら、git rebase —continueを実行してください
* 現在は修正待ちの状態ということ

```text
warning:  stopped at …add Fx BB()… ①
You can amend the commit now, with…②

        git commit —amend

Once you are satisfied with your changes, run…③

        git rebase —continue
```

* 変更したいコミットが一時的にHEADになっていることを確認する

```bash
git log —oneline —decorate
```

```text
2501611(HEAD) add Fx BB()
795341c add Fx AA()
```

```bash
vim function.php #エディタでファイルの内容に変更を加える
git add .
git commit —amend #amendオプションでコミットする
git rebase —continue
```

```text
Successfully rebased and updated refs/heads/rebaseEdit
```

```bash
#HEADが最新のコミットに戻っていることを確認する
git log —oneline —decorate
#マスターブランチに戻る
git checkout master
#masterに戻ったことを確認する
git branch
```

### 注意

* 過去のコミットの変更が許可される基準
    * 他人が作ったコミットを含む履歴の変更はNG
        * 他人が作ったコミット: git pull・git fetchで取得したコミット
    * 一度公開をしたコミットを含む履歴の変更はNG
        * 一度公開をしたコミット: git pushした時点のすべてのコミット
    * 未公開の自分が作ったコミットしかない履歴の変更はOK
        * git pushする前の自分が作ったコミットしかない履歴の変更はOK

