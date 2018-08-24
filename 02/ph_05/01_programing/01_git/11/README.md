# 問題

## 以下のツリーを作成する

```bash
git tree
```

```text
*       AKI     3064747  (HEAD) commit from v0.1 02
*       AKI     72c7b86  commit from v0.1
| *     AKI     338e329  (refs/stash) WIP on master: 98cc33b checkout master and add commit
| |\
| | *   AKI     af5247b  index on master: 98cc33b checkout master and add commit
| |/
| *     AKI     98cc33b  (master) checkout master and add commit
|/
| *     AKI     d30738a  (next) add commit from next
| *     AKI     3468e02  commit from next branch after create branch next
|/
*       AKI     ca45905  (tag: v0.1) frist commit from master branch
```

## ヒント

```bash
cat sample.txt
```

```text
master01
<<<<<<< Updated upstream
=======
master02
master03
>>>>>>> Stashed changes
v0.1 01
v0.1 02
```

## 解答

```bash
mkdir local
cd local
git init
echo "master01" > sample.txt
git add sample.txt
git commit -m "frist commit from master branch"
git tree

git tag v0.1
git tree

git checkout -b next
echo "next01" >> sample.txt
git commit -am "commit from next branch after create branch next"
git tree

echo "next02" >> sample.txt
git commit -am "add commit from next"
git tree

git checkout master
echo "master02" >> sample.txt
git commit -am "checkout master and add commit"
git tree

echo "master03" >> sample.txt
git stash
git tree

#v0.1に戻る
git checkout v0.1
```

* detached HEAD = ( no branch )状態であると警告される

```text
Note: checking out ‘v0.1’ .

You are in ‘detached HEAD’ state. You can look around, make experimental 
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may 
do so  ( now or later ) by using -b with the checkout command again. Example:

    git checkout -b <new-branch-name>

HEAD is now at 3da8500.. first commit from master branch
```

```bash
#元の作業状態に戻る
git stash pop
```

```text
Auto-merging sample.txt
CONFLICT ( content ) : Merge conflict in sample.txt
```

```bash
echo "v0.1 01" >> sample.txt
git commit -am "commit from v0.1"

echo "v0.1 02" >> sample.txt
git commit -am "commit from v0.1 02"
git tree
```

```text
*       AKI     722e4f4  (HEAD) commit from v0.1 02
*       AKI     e446644  commit from v0.1
| *     AKI     6b90ae9  (refs/stash) WIP on master: e9d106f checkout master and add commit
| |\
| | *   AKI     4d8cc84  index on master: e9d106f checkout master and add commit
| |/
| *     AKI     e9d106f  (master) checkout master and add commit
|/
| *     AKI     826303e  (next) add commit from next
| *     AKI     b744500  commit from next branch after create branch next
|/
*       AKI     7aea767  (tag: v0.1) frist commit from master branch```
```

* 最新のコミットには( HEAD )しか目印がない
    * ( HEAD )がnextに移動する	
    * 目印の付いていなかった最新コミットは見えなくなってしまう。	
    * ログの本質は何らかの目印(ブランチやタグ)を基準にコミットをたどる仕組み。	
    * そのため、目印が何も付いていないコミットは消えたように見えてしまう。	
    * このようなコミットは一定期間は保存されるが、いずれ削除されてしまう。	
    * 長期間目印がない＝不要なコミットと判断される	

### 最新コミットに目印をつける

```bash
#next ブランチに戻る
git checkout next
```

```text
Warning: you are leaving 2 commits behind, not connected to
any of your branches:

  3064747 commit from v0.1 02
  72c7b86 commit from v0.1

If you want to keep them by creating a new branch, this may be a good time
to do so with:

 git branch <new-branch-name> ${ハッシュ}

Switched to branch 'next'
```

```bash
HASH=${ハッシュ}
```

```bash
#最新のコミットが見えないことを確認する
git tree
#１つ目の無名ブランチの記録を確認する
git log --oneline ${HASH} | grep 'commit from v0.1' | tail -1 | cut -f 1 -d ' ' | xargs git show
```

```text
diff --git a/sample.txt b/sample.txt
index 3406cd7..956a13e 100644
--- a/sample.txt
+++ b/sample.txt
@@ -1 +1,7 @@
 master01
+<<<<<<< Updated upstream
+=======
+master02
+master03
+>>>>>>> Stashed changes
+v0.1 01
```

```text
master ブランチに戻り
master02とmaster03を追記し、一時保存

v0.1に戻り、
master02とmaster03を取り戻した後に
v0.1にてv0.1 01を追記した

という意味
```

```bash
#２つ目の無名ブランチの記録を確認する
git log --oneline ${HASH} | grep 'commit from v0.1 02' | cut -f 1 -d ' ' | xargs git show
```

```text
diff --git a/sample.txt b/sample.txt
index 956a13e..ff1eb3d 100644
--- a/sample.txt
+++ b/sample.txt
@@ -5,3 +5,4 @@ master02
 master03
 >>>>>>> Stashed changes
 v0.1 01
+v0.1 02
```

```text
>>>>>>> Stashed changes以下は
stash pop後の作業履歴
```

```bash
#最新コミットを指定し、チェックアウト
git log --oneline ${HASH} | grep 'commit from v0.1 02' | cut -f 1 -d ' ' | xargs git checkout
```

```text
Note: checking out '3064747'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 3064747... commit from v0.1 02
```

## 完成

```bash
git tree
```

```text
*       AKI     3064747  (HEAD) commit from v0.1 02
*       AKI     72c7b86  commit from v0.1
| *     AKI     338e329  (refs/stash) WIP on master: 98cc33b checkout master and add commit
| |\
| | *   AKI     af5247b  index on master: 98cc33b checkout master and add commit
| |/
| *     AKI     98cc33b  (master) checkout master and add commit
|/
| *     AKI     d30738a  (next) add commit from next
| *     AKI     3468e02  commit from next branch after create branch next
|/
*       AKI     ca45905  (tag: v0.1) frist commit from master branch
```

```bash
cat sample.txt
```

```text
master01
<<<<<<< Updated upstream
=======
master02
master03
>>>>>>> Stashed changes
v0.1 01
v0.1 02
```

## rebase

```bash
#HEADとnextの共通の祖先(v0.1)を起点に、HEADのコミットを２つをnextに移動する
git rebase next
```

```text
First, rewinding head to replay your work on top of it...
Applying: commit from v0.1
Using index info to reconstruct a base tree...
M	sample.txt
Falling back to patching base and 3-way merge...
Auto-merging sample.txt
CONFLICT (content): Merge conflict in sample.txt
error: Failed to merge in the changes.
Patch failed at 0001 commit from v0.1
The copy of the patch that failed is found in: .git/rebase-apply/patch

Resolve all conflicts manually, mark them as resolved with
"git add/rm <conflicted_files>", then run "git rebase --continue".
You can instead skip this commit: run "git rebase --skip".
To abort and get back to the state before "git rebase", run "git rebase --abort".
```

```bash
cat sample.txt
```

```text
master01
<<<<<<< HEAD             #nextブランチの内容
next01
next02
=======
<<<<<<< Updated upstream #masterブランチの内容
=======
master02
master03
>>>>>>> Stashed changes  #no branchブランチの内容
v0.1 01
>>>>>>> commit from v0.1
```

```bash
vim sample.txt
```

* 下記のように編集

```text
master01
next01
next02
v0.1 01
```

```bash
#stashがないときは以下でも可 今回は v0.1 01 が消えてしまう
#git checkout --ours sample.txt
```

```bash
cat sample.txt

git add sample.txt
#rebaseを終了する
git rebase --continue
```

```text
Applying: commit from v0.1
Applying: commit from v0.1 02
Using index info to reconstruct a base tree...
M	sample.txt
Falling back to patching base and 3-way merge...
Auto-merging sample.txt
```

* next_tmpというブランチを作成する	
    * これは新規作成というよりも、現在の無名ブランチに名前をつけるという意味	
    * 今のHEADの位置を見失わないため	

```bash
git branch next_tmp
#nextブランチをチェックアウト
git checkout next
```

```text
Previous HEAD position was … commit from v0.1 02
Switched to branch ‘next’
```

```bash
#next_tmpをnextにmergeする
git merge next_tmp
```

```text
Updating d30738a..d27fba6
Fast-forward
 sample.txt | 2 ++
 1 file changed, 2 insertions(+)
```

```bash
cat sample.txt
```

```text
master01
next01
next02
v0.1 01
v0.1 02
```

```bash
#ログのHEADを確認する
git tree
```

```text
*       AKI     d27fba6  (HEAD -> next, next_tmp) commit from v0.1 02
*       AKI     4231c19  commit from v0.1
*       AKI     d30738a  add commit from next
*       AKI     3468e02  commit from next branch after create branch next
| *     AKI     338e329  (refs/stash) WIP on master: 98cc33b checkout master and add commit
| |\
| | *   AKI     af5247b  index on master: 98cc33b checkout master and add commit
| |/
| *     AKI     98cc33b  (master) checkout master and add commit
|/
*       AKI     ca45905  (tag: v0.1) frist commit from master branch
```

```bash
#stashを削除する
git stash drop
```

```text
Dropped refs/stash@{0} (338e329ae45c6d5d22bd45e6407cd7e48e814d1b)
```

```bash
git tree
```

```text
*       AKI     d27fba6  (HEAD -> next, next_tmp) commit from v0.1 02
*       AKI     4231c19  commit from v0.1
*       AKI     d30738a  add commit from next
*       AKI     3468e02  commit from next branch after create branch next
| *     AKI     98cc33b  (master) checkout master and add commit
|/
*       AKI     ca45905  (tag: v0.1) frist commit from master branch```

