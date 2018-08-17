# グループ操作

* グループを作成するには、groupaddコマンド
* グループにユーザーを追加するには、usermodコマンド
* グループを削除するには、groupdelコマンド

## グループを操作

### グループを作成

* `groupadd` コマンド

```bash
groupadd グループ名
```

次の例では、testグループを作成

```bash
groupadd test
```


### 作成されたか確認

* `/etc/group` の最終行に追加される

```bash
cat /etc/group | grep 'test'
test:x:1000:
```

## グループにユーザーを追加

* `usermod`コマンド
    * USER MODify
    * `/etc/passwd` のユーザー情報を変更する際に使うコマンド
        * ユーザーのデフォルトシェルやホームディレクトリを変更するなど
    * `G` オプション
        * セカンダリグループとして追加
    * `g` オプション
        * ユーザーのプライマリグループが変更される

```bash
usermod -G グループ名 ユーザー名

#例: studentユーザーをtestグループに追加
usermod -G test student
#確認
id student # 元のグループに追加で新規グループも追加されていることを確認
uid=1000(student) gid=1001(student) groups=1001(student),1000(test)
# groupファイルからも確認できる
grep 'test' /etc/group
test:x:1000:student
```

## グループを削除

* `groupdel` コマンド

```bash
groupdel グループ名
```

* ユーザーのプライマリグループは削除`不可`
    * ライマリグループを削除してしまうと、どのグループにも属さないユーザーが現れてしまう可能性があるため

```bash
groupdel test
```
