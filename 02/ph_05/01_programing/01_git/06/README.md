# リモートリポジトリで作業する

* remote.gitとlocalとfriendの３ディレクトリを作り直す
    * remote.gitは.gitを付ける

```bash
mkdir remote.git local friend
cd ../
ls -al
```

* 権限を確認する→グループに対して書き込み権限がない

```text
rwxr-xr-x
```

* ベアリポジトリとして初期化する
    * `—bare`
        * 作業ファイルのないGit管理フォルダになる
        * 今まではディレクトに.gitというディレクトリがありそこで全て管理していた
    * `--shared`
        * ディレクトリ内の全ファイルをグループで読み・書き可能な権限に設定して初期化する

```bash
cd remote.git
git init —bare —shared
git config -l #core.sharedrepository=1が設定されていることを確認する
```

* `core.sharedrepository=1`の意味
    * Gitはリポジトリ初期化後に新規作成されるファイル・フォルダについてもグループの書き込み権限を有効にしてくれる
    * もしumaskが022のまま、誰かがうっかり共有リポジトリを更新してしまうと、そのユーザー以外は書き込みできないファイルが追加されてしまうかもしれない
* 手動で設定する場合は以下

```bash
git config core.sharedrepository 1
```

* １つ上の階層に戻り、グループの権限が変化していることを確認する

```bash
cd ../
ls -al
```

```text
rwxrwsr-x
```

## リモートリポジトリにpushする

```bash
cd ../local
git init
git push
```

* 下記のエラーが出ることを確認する
    * 何も行なっていない状況でプッシュするとエラーになる
```text
No refs in common and none specified; doing nothing.
Perhaps you should specify a branch such as ‘master’
```

```bash
touch sample.txt
git add .
git commit -m "first commit"
#project.git(リモートディレクトリ)にプッシュする
git push —all ../remote.git/

git log —oneline
cd ../remote.git
#一致していることを確認する
git log —oneline
cd ../
rm -rf local/
#再度lcoalディレクトリを作成する
mkdir local
cd local
#project.gitからクローンしてくる
git clone ../remote.git . #今後はpush・pullでパスの指定が不要になる
```

## 友人側から共有リポジトリ(gitフォルダ)にアップロードする

```bash
cd ../
mkdir friend
cd friend
```

```bash
#friend
git clone ../remote.git .
git checkout -b friendDevelop
git branch
vim 既存ファイル #既存ファイルに修正を加える
git commit -am "friend側から修正"
git checkout master
git merge friendDevelop
git push
```

```bash
#local
git pull
git tree
#変更された内容を確認する
git show 
```

### 自分のアップロードが後出しになってしまった場合…マージ

* git pushが失敗した時は、ファストフォワードな関係にしておく必要がある
    * git pull、あるいはgit fetch&git mergeによって、一旦マージして
* git pushは自動マージしてくれないので、気を付ける

```bash
#friend
vim 既存ファイル #既存ファイルに修正を加える
git diff
git commit -am "friends commit"
git push
```

```bash
#local
vim 既存ファイル
git commit -am "local commit"
git push #失敗する
```

```text
! [ rejected ]   master -> master ( non-fast-forward )
```

```bash
#最新のリポジトリを取ってくる
git fetch
```

```text
remote : Counting objects : 3, done.
remote : Total 3 ( delta 0 ), reused 0 ( delta 0 )
Unpacking objects : 100% (3/3) , done.
From  C:/Users/aki/esktop/git_practice/…
75867e0…5f2f805 master  -> origin/master
```

```text
git tree #状況を確認する
git diff HEAD origin/HEAD #自分のリポジトリに含まれていない変更を確認する
git merge origin/master #変更を取り込む
```

```text
"Auto-merging sample.txt
CONFLICT (content) : Merge conflict in sample.txt
Automatic merge failed; fix conflicts and then commit the result."
```

### oursとtheirs

```bash
git checkout —ours sample.txt   # —ours とすることで前半を採用できる
git checkout —theirs sample.txt # —theirs とすることで後半を採用できる
git diff
git commit -a
tree #状況を確認
#改めてプッシュする
git push
```

## 追跡ブランチ

* git fetch
    * 追加されたリモートブランチを追加する

```bash
#friend
git branch AA
#AAブランチをリモートにプッシュする
git push ../remote/ AA
#リモートブランチにAAが追加されていることを確認する
git branch -a
```

```text
* master
  remotes/origin/AA
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/testBranch
  remotes/origin/testBranch2
```

```bash
#local
#friend側で作成してプッシュしたリモートブランチの存在確認
git branch -a
```

* 見つからない
    * リモートブランチには確かに追加されていたはず

```text
* master
 remotes/origin/HEAD -> origin/master
 remotes/origin/master
 remotes/origin/testBranch
 remotes/origin/testBranch2
```

```bash
git fetch
```

```text
remote : Counting objects : 3, done.
remote : Total 3 ( delta 0 ), reused 0 ( delta 0 )
Unpacking objects : 100% (3/3) , done.
From  C:/Users/aki/esktop/git_practice/…
* [new branch] AA  -> origin/AA
```

```bash
git branch -a
```

* 再度リモートブランチを確認すると反映されている

```text
* master
 remotes/origin/AA
 remotes/origin/HEAD -> origin/master
 remotes/origin/master
 remotes/origin/testBranch
 remotes/origin/testBranch2
```

* リモートブランチが表示されているのであれば、fetchせずとも表示されていてもいいのでは？？
    * 実は、git branch -aで表示されているものはリモートブランチではない	
    * 正体は、追跡ブランチと呼ばれるもの	
        * リモートブランチの情報を持っているローカルリポジトリの中の特殊なブランチ	
        * 追跡ブランチは、ローカルに存在しているのでローカルブランチの一種	
* git branch -aで表示しているのはリモートブランチの情報を持っているローカルリポジトリの中の特殊なブランチの一覧	

```text
* [new branch] AA  -> origin/AA
```
	
* 「リモートリポジトリにある AAというブランチから、ローカルリポジトリにorigin/AAという追跡ブランチを作ったよ」ということを表している	

```bash
#チェックアウトできることを確認
git checkout AA
```