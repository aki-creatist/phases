# 管理者用のパスワード設定

## 管理者として接続する

* MySQLサーバで操作する場合、`root`ユーザーで接続可能
    * `root`: 管理者権限を持ち全ての操作が可能な特別なユーザ
* 初期状態では`root`ユーザのパスワードは未設定
    * セキュリティ面で危険
* パスワードを設定する
    * rootのパスワード設定には同じくMySQL CLIツールを利用する

```bash
#mysql -u ユーザー名 -p # `-p` はパスワードを使用すると言う意味
mysql -u root -p
#Enter password: #何も入力せずEnterキーのみ押す
```

## パスワードを設定するSQL

* MySQLに既に登録されているユーザに対してパスワードを割り当てる
    * `SET PASSWORD`ステートメントを実行する
    * MySQLサーバではログインするユーザーを`ユーザー@ホスト名`のようにホスト名とセットにして管理している
    * ホスト名の代わりにIPアドレスで指定することも可能
        * `ホスト名`: ネットワークに接続された機器に分かりやすく名前をつけたもの
        * 今操作しているパソコンまたはサーバはlocalhost

```sql
SET PASSWORD FOR ユーザー名@ホスト名=PASSWORD('パスワード');
```

## パスワードを設定する

* MySQL CLIツールを起動
* rootで接続
* SQLを入力
    * ユーザーの指定は`root@localhost`
        * `rootはMySQLサーバが動作しているlocalhostから接続する`の意味
* `Query OK`と表示されたら、「root」にパスワードが設定完了
    * `quit`と入力してMySQL CLIツールを終了する

```sql
--passwordには任意のパスワードを記述
SET PASSWORD FOR root@localhost=PASSWORD('password');
```

## パスワードを使って接続する

* 再度MySQL CLIツールをrootで起動
* `Enter password:`に続けて前の手順で設定したパスワードを入力
* Enterキーを押すとMySQLサーバに接続する

```bash
#mysql -u ユーザー名 -p # `-p` はパスワードを使用すると言う意味
mysql -u root -p
#Enter password: #設定したパスワードを入力
```