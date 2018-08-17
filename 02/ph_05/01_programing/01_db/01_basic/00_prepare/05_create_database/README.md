# DBの作成

* データを保管するDBを作成する
* DBに接続するための権限の設定をする

## CREATE DATABASE文

* 新規にDBを作成する
    * DB名は最長64バイト
    * 日本語名でも作成可能だが半角英数字や記号で作成するべき
* デフォルトでは以下のようになる
    * 文字コード: `latin1`
    * COLLATE(照合順位): `latin1_swdish_ci`

```sql
CREATE DATABASE DB名;
```

## 文字コードと照合順序の指定

* 文字コードはUTF-8で統一したい
* 照合順位も一緒に設定
    * utf8_general_ci: ciというのは大文字と小文字を区別しない
        * utf8-general-ci：比較条件の拡張なし
        * utf8-unicode-ci：比較条件の拡張あり
            * ひらがなの「ほ」で条件を指定した際「ぼ」や「ボ」や「ホ」といったものに一致

```sql
CREATE DATABASE DB名
CHARACTER SET 文字コード名 COLLATE 照合順位;
```

## DBを作成する

* MySQL CLIツールをroot権限で起動
* プロンプト`mysql>`が表示される
* `CREATE`文を実行
    * DB名: `sampledb`
    * 文字コード: `utf8`
    * 照合順位: `utf8_general_ci`
* `Query OK`と表示されたらDB作成に成功

```sql
CREATE DATABASE sampledb CHARACTER SET utf8 COLLATE utf8_general_ci;
```

## DBを確認する

### SHOW DATABASES文

* DBが作成されたか確認する
* `SHOW`文を使用する
    * SHOW構文を使えば、この他に以下のような操作が可能
        * テーブル(データを入れる表のようなもの)を一覧
        * カラム(データを一つ一つ入れる場所)を一覧
        * サーバのステータス情報など一覧

```sql
SHOW DATABASES;
```

## DBの削除

### DROP DATABASE文

* 不要なDBは`DROP DATABASE`文で削除可能
* DB内にデータが蓄積されている場合、含まれているデータなども一緒に完全に消えてしまうので操作には注意が必要

```sql
DROP DATABASE DB名
```

### 手順

sampledbを削除する

* MySQL CLIツールに`root`で接続
* プロンプト`muysql>`が表示されたらSQLを実行
* `Query OK`と表示されたらDBの削除が成功

```sql
DROP DATABASE sampledb;
```

## USE文

* これから目的のDBを利用するということをMySQLサーバに伝える

```sql
--USE DB名;
USE sampledb;
```
