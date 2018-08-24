# 変更の衝突

```bash
#local
echo "local02" >> sample.txt
git commit -am "local02"
#friend
echo "friend02" >> sample.txt
git commit -am "friend02"
#local
git pull ../friend/ #コンフリクト発生
cat sample.txt
```

```text
<<<<<<<<HEAD
local02
=======
friend02
>>>>>>>>aa50e4232…………
```

```bash
#local
vim sample.txt
git commit -am "local側からlocalを優先"
git log —oneline
```

```text
b1ff63 (HEAD -> master) local側からlocalを優先
aa50e43 friend02
54b7ce8 local02
b58f7b0 friend01
b5778ac local01
```

```bash
#friend
git pull #変更を取り込む
git log —oneline
```

```text
b1ff63 (HEAD -> master , origin/master, origin/HEAD) local側からlocalを優先
aa50e43 friend02
54b7ce8 local02
b58f7b0 friend01
b5778ac local01
```

```bash
#friend
git log —oneline —graph
```

```text
*     b1ff63 (HEAD -> master , origin/master, origin/HEAD) local側からlocalを優先
| \
|   *  aa50e43 friend02
*   |  54b7ce8 local02
|  / 
*  b58f7b0 friend01
*  b5778ac local01
```

## マージコミットを残す

```bash
#local
echo "local04" >> sample.txt
git commit -am "local04"
#friend
echo "friend04" >> sample.txt
git commit -am "friend04"
#local
git pull ../friend/ #コンフリクトメッセージが表示される
git commit -a #viが起動するので、:wqで保存
git log —oneline
```

```text
70fee16 Merge ../friend into HEAD
be5c44f friend04
183d4f6 local04
b1ff63 (HEAD -> master) local側からlocalを優先
aa50e43 friend02
54b7ce8 local02
b58f7b0 friend01
b5778ac local01
```

```bash
#local
vim sample.txt
git commit -am "localを優先" #localの変更を優先して保存
git log —oneline
```

```text
9342c85 (HEAD -> master) localを優先
70fee16 Merge ../friend into HEAD
be5c44f friend04
183d4f6 local04
b1ff633 local側からlocalを優先
aa50e43 friend02
54b7ce8 local02
b58f7b0 friend01
b5778ac local01
```

```bash
#friend
git pull #変更を取り込む
```

## リモート設定をする

* なぜfriendはgit pullにパスを指定しなくていいのか

```bash
#local
git config -l #設定を表示する
#friend
git config -l #下から４行を比較する
```

### local

* ブランチ未指定の場合、相手の作業ブランチを指す
* 本来はmaster同士の場合にはmasterを指定する
* 相手の作業ブランチをマスターに取り込んでしまうため

```bash
#local
git pull ../friend/ #masterを省略して書いている
```

### friend

* git pull origin master と書くことができる
    * remote.origin.url=../local/の設定がされているため
    * origin=../localと解釈される
* git pullと書くこともできる
    * masterブランチでpullした場合のデフォルトが、origin masterになる
    * `branch.master.remote=originとbranch.master.merge=ref/heads/master`
    * つまり、origin masterが省略されると自動的にorigin masterが捕捉される

```bash
git pull #friend側のgit pullは正確には、git pull ../local master となる
```

### local

```bash
git remote add friend ../friend/ #friendを追加
git remoet -v #確認
git config -l #確認
git fetch friend
```

```text
From ../friend
*[new branch] master -> friend/master
```

```bash
git branch —set-upstream master friend/master
git config -l
```

* 以下が追加されていることを確認する"

```text
branch.master.remote=friend
branch.master.merge=refs/heads/master
```

```bash
git pull #Already up-to-date と表示されれば成功
```
