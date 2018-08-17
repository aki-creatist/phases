# CREATE TABLE文

* `CREATE TABLE テーブル名 ();`が基本
* `()`の中に各カラムの指定を行う
* カラム名は自分で作成する
* カラム名から半角スペースで区切って、MySQLで決められているデータ型を設定する
* 各カラムとプライマリキーは`,`で繋ぐ

```sql
--CREATE TABLE文の構造
CREATE TABLE テーブル名(
カラム名 データ型,
カラム名 データ型,
プライマリキー
);
```

* データ型
    * [整数型](01_int)
    * [文字列型](02_varchar)
* [プライマリキー](03_primary)
* [ストレージエンジンの指定](04_strage)

### 手順

* MySQL CLIツールで、ユーザーsampleで接続
* プロンプト`mysql>`が表示されたら、`use sampledb;`を実行
    * sampledbに接続
* SQLを実行する
    * テーブル名: members
    * カラム名: `id`
    * データ型: `MEDIUMINT UNSIGNED`
        * 会員番号は１から始まる整数にするため整数型

```sql
CREATE TABLE member(
id        MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
last_name VARCHAR(50),
first_name VARCHAR(50),
PRIMARY KEY(id)
);
```