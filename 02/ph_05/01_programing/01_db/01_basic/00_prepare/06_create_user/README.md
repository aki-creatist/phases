# ユーザー作成

* MySQLサーバを操作する専用のユーザーを作成する
* プログラムから接続する時はこのユーザーを利用する

## 背景

* rootはMySQLサーバに関する操作全般を行う時の専用ユーザー
* プログラムからrootで接続することもできるが安全性を高めるため別のユーザーを作成する

## CREATE USER文

* 最大文字数
    * ユーザー名: 最大16文字
    * ホスト名: 最大60文字
    * パスワード: 最大41文字
* 半角英数字や記号を使用する
* `'`(シングルクォーテーション)」で`ユーザー名@ホスト名`を囲む

```sql
CREATE USER 'ユーザー名'@'ホスト名' IDENTIFIED BY 'パスワード';
```

### 手順

* MySQL CLIツールを起動して`root`で接続
* プロンプト`mysql>`が表示されたらSQLを実行
    * ユーザー名: `sample`
    * ホスト名: `localhost`
    * パスワード: `password`
        * ネットワーク介して外部から接続するような時にはここにIPアドレスを設定する
* `Query OK`と表示されたらユーザーの追加に成功

```sql
CREATE USER 'sample'@'localhost' identified BY 'password';
```

## ユーザーの削除

* `DROP USER`文を使用する
* ユーザー作成と同様にユーザー名とホスト名のセットを指定する

```sql
DROP USER 'sample'@'localhost';
```

## 追加したユーザーで接続する

### 手順

* MySQL CLIツールを終了
* ユーザーを`sample`に変更してMySQLサーバに接続する
* プロンプト`mysql>`が表示されたら成功

```sql
--一度CLIツールを終了
quit
mysql -u sample -p
```