# 権限を設定する

## GRANT文

* 作成したユーザーに対して、MySQLに接続するための権限を細かく設定可能
    * DBだけではなくテーブルやカラム単位で権限を設定も可能
* `GRANT`直後に権限を指定
    * `*`はワイルドカード

```sql
GRANT 権限 ON データベース名.* TO 'ユーザー名'@'ホスト名';
```

正式には以下

```sql
GRANT ALL PRIVILEGES ON `DB名`.テーブル TO 'ユーザ名'@'ホスト名';
GRANT SELECT,UPDATE,INSERT,DELETE ON `DB名`.テーブル TO 'ユーザ名'@'ホスト名';
```

## ユーザーにデータベース権限を設定する

### 手順

* MySQL CLIツールに`root`として接続
* SQLを実行
    * 権限: ALL PRIVILEGES(全ての権限)
    * 対象:sampledb.*
    * 権限を追加するユーザー: `sample`
    * ホスト名: `localhost`
* 権限を変更したら`FLUSH`構文で内部キャッシュされている権限をクリア
    * 新しい権限を再度読み込む

```sql
GRANT ALL PRIVILEGES ON sampledb.* TO 'sample'@'localhost';
flush plivileges;
```

## データベースに接続する

### 手順

* MySQL CLIツールを終了
* `sample`ユーザで MySQL CLIツールを起動
* プロンプト`mysql>`が表示されたら`use sampledb;`
* `Dataase changed`と操作対象のデータベースが切り替われば成功

```sql
quit

mysql -u sample -p

USE sampledb;
```
