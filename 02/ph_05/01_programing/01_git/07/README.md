# merge

* fetchはリモートの変更を追跡ブランチに反映させてくれるが、その変更をローカルに反映しない	
* リモートの変更を反映させるにはmergeが必要になる

```bash
#friend
git checkout testBranch
vim 既存ファイル
git commit -am "will conflict"
git push origin testBranch
```

```bash
#local
#コンフリクトを起こしたいので既存ファイルを編集する
vim 既存ファイル
#リモートの変更を追跡ブランチ反映する
git fetch 
#friend側の変更を確認したいので追跡ブランチに移動する
git checkout origin/testBranch
```


```text
error: Your local changes to the following file would be overwritten by checkout 
    test.txt
Please commit your changes or stash them before you merge.
Aborting

意訳
チェックアウトであなたの追跡ファイルに対する変更は書き換えられるだろう
まずはコミットするかスタッシュしてほしい。
一時中断するよ。
```

```bash
git merge origin/testBranch
```

```text
error: Your local changes to the following file would be overwritten by checkout 
    test.txt
Please commit your changes or stash them before you merge.
Aborting

意訳
チェックアウトであなたの追跡ファイルに対する変更は書き換えられるだろう
まずはコミットするかスタッシュしてほしい。
一時中断するよ。
```

```bash
#指示に従い、まずはコミットする
git commit -am "conflict"
```

* ひとまずは何も怒られない

```text
1 file changed, 1 insertion(+)
```

```bash
#改めてマージする
git merge origin/testBranch
```

```text
Auto-merging test.txt
CONFLICT (content) : Merge conflict in test.txt
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
cat test.txt                #ファイルの中身を確認
git checkout —ours test.txt #コンフリクトを解消
git commit -m "ok"          #コンフリクト解消後に改めてコミットする
git push origin testBranch  #コンフリクト解消後に改めてプッシュする
git tree                    #マージされていることを確認する
```

## リモートブランチの削除

```bash
#リモートブランチを削除する
git push origin :testBranch2
#削除できたことを確認してみる
git branch -a
#ローカル側のtestBranch2も削除しておく
git branch -d testBranch2
git checkout master 
```

## 他人に行われたリモートブランチの削除を反映する

```bash
#friend
#友達が共有ディレクトリのリモートブランチを削除してしまった。を再現。
git push origin :testBranch
#testBranchが削除されていることを確認する
git branch -a
```

```bash
git branch -a
```

* pullする前なので当然ブランチの削除は反映されていない

```text
* master
  testBranch
  remotes/remote/master
  remotes/remote/testBranch
```

```bash
#local
git pull remote master
#リモートで何が起こったのかを確認する
git remote show remote
```

* 上記の内、Remote branches : の項目を確認する
* testBranchがstale=無効なブランチと表示されている
  
```text
remote remote
Fetch URL : ../remote.git/
Push  URL : ../remote.git/
HEAD branch : master
Remote branches :
  master                tracked
  refs/remotes/remote/testBranch stale (use ‘git remote prune’ to remove)
Local ref configured for ‘git push’ : 
  master pushed to master (up to date)
```

```bash
#変更を反映する
git remote prune remote
```

```text
Pruning remote
URL : ../remote.git/
*  [pruned] remote/testBranch
```

```bash
git branch -a #リモートブランチを確認する
```

* 無事に削除が反映されたことが確認できればOK

```text
* master
  testBranch
  remotes/remote/master
```