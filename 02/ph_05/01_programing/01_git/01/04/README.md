# 打ち消しコミットを生成する(revart)

```bash
vim function.php
```

```text
"<?php

function AA(){}

?>"
```

```bash
git add .
git commit -m "add Fx AA()"
```

```bash
vim function.php
```

```text
"<?php

function AA(){}
function BB(){}
?>"
```

```bash
git commit -am "add Fx BB()"
```

```bash
vim function.php
```

```text
"<?php
function CC(){}
function AA(){}
function BB(){}
?>"
```

```bash
git commit -am "add Fx CC()"
```

```bash
git log —oneline
```

```text
"f56574b(HEAD) add Fx CC()
2501611 add Fx BB()
795341c add Fx AA()"
```

```bash
#revertブランチを生成する
git branch revert
#ブランチが生成できたことを確認する
git branch
#ブランチを移動する
git checkout revert 
```

### revertブランチ

```bash
#ブランチが移動していることを確認する
git branch
#add Fx BB()のIDを指定する vimが開く
git revert 2501611
```

↓下記のように修正

```text
Revert "delete Fx BB" 
```

↓下記のようなメッセージが表示される

```text
"[detached HEAD 1e98321] Revert "delete Fx BB()"
1 file changed, 1 insertion(+), 1 deletion(-)"
```

```bash
#function BB()が打ち消されていることを確認する
cat function.php
```

```text
"<?php
function CC(){}
function AA(){}

?>"
```

```bash
#ログを確認する
git log —oneline
#マスターブランチに戻る
git checkout master
```

### masterブランチ

```bash
#マスターブランチに戻ったことを確認する
git branch
```

## いくつか前のコミットを削除する (rebase)

```bash
#rebaseブランチを生成する
git branch rebase
#ブランチが生成できたことを確認する
git branch
#ブランチを移動する
git checkout rebase 
```

### rebase ブランチ

```bash
#ブランチが移動していることを確認する
git branch
git log —oneline
```

```text
"f56574b(HEAD) add Fx CC()
2501611 add Fx BB()
795341c add Fx AA()"
```

```bash
#修正したいコミットの１つ前を指定する
#add Fx BB()を削除したいので、add Fx AA()のIDを指定する
git rebase -i 795341c
```

```text
pick 2501611 add Fx BB()
pick f56574b add Fx CC()
```

* `pick`: これに続くコミットを変更しないで、そのまま利用するという意味のコマンド

* `p`, `pick`: コミットを利用する。
* `r`, `reword`: コミットを利用するが、コミットメッセージは編集する。
* `e`, `edit`: コミットを利用しますが、修正のため一時停止する。
* `s`, `squash`: コミットを利用しますが、前のコミットと合体する。
* `f`, `fixup`: "squash"に似ているが、コミットメッセージは破棄する。
* `x`, `exec`: シェルコマンドを実行する

行の並べ替えは可能で、上から下に実行されます。

ここで一行削除すると、そのコミットは削除されます。
けれども、全てを削除した場合は、rebaseは中止されます。

```text
1. pick 2501611 add Fx BB() の行を削除
2. 起動したエディタで指定の行を削除し、保存する
```

```text
Successfully rebased and updated refs/heads/rebase
```

```bash
#削除を意図したコミットが削除されていることを確認する
git log —oneline
```

```text
"f56574b(HEAD) add Fx CC()
795341c add Fx AA()"
```

```bash
#function BB(){}が消えていることを確認する
cat function.php
#マスターブランチに戻る
git checkout master 
```

### master ブランチ

```bash
#マスターブランチに戻ったことを確認する
git branch
```