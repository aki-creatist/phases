# スタッシュ

* 一時退避

```bash
echo 1 > sample.txt
git add .
git commit -m "1st commit"
#追加書き込み
echo 2 >> sample.txt
git stash #作業が一時保存される
```

```text
Saved working directory and index state WIP on master
```

```bash
cat sample.txt
git stash list
```

```text
stash@{0} WIP on master : 048450c 1st commit
```

```bash
#最新の作業環境を復元する
git stash pop
#スタッシュリストから削除されていることを確認する
git stash list
#スタッシュに名前をつけて一時保存
git stash save ‘スタッシュに名前をつける’
#スタッシュの保存状態を確認する
git stash list
```

```text
stash@{0}: On master:スタッシュに名前をつけて一時保存
```

```bash
#最新状態を復元する
git stash apply
#スタッシュリストの中に記録が残っていることを確認する
git stash list
#スタッシュがツリーにどのような表示がされるかを確認する
git tree
#復元したものをコミットする
git commit -am "after stash"
git tree
#リストを削除する
git stash drop
git tree
```

# reflog

* 操作の詳細なログを確認する

```bash
git reflog
```