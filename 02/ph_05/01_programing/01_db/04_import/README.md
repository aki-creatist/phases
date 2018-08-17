# ファイルでSQL文を実行

## csvファイルの読み込み

```sql
--csv読み込み
postgres=# copy テーブル名 from 'ファイルパス' with csv;
```

## 背景

* テーブル作成が多数ある
* MySQL CLIツールで入力するのに時間がかかる

## 方法

* MySQL CLIツールからファイルのSQL文を流し込む方法
* 接続した後に読み込む方法

## 手順1

* SQL文(CREATE TABLE文などのこと)をファイルに保存
* 接続する前に読み込む

## 手順2

* SQL文をファイルに保存
* 接続した後に読み込む

## SQL文をファイルに保存

* SQL文を名前をつけたファイルに文字コードUTF-8で保存
    * 場所はフルパスで指定

```bash
vim work.sql
```

## 方法1: 接続した後に読み込む

* `データベース名 < ファイル名`としてリダイレクト

```
#リダイレクト機能を利用して流し込む
mysql -u sample -p sampledb < work.sql
--エラーが出ていなければ成功
```

## 方法2: 接続した後に読み込む

* コマンドの後にファイル名`word.sql`を同様にフルパスで指定して読み込む
* 利用するコマンド
    * Windows: `¥.`
    * Mac、Linux: `\.`

```sql
--使用するDBを指定
USE sampledb;
--Emptyであることを確認
SHOW TABLES;
--外部ファイル読み込み
\. work.sql
--テーブルが作成されていることを確認
SHOW TABLES;
```

## 備考

Windowsの場合、コマンドプロンプトからUTF-8のファイルを読み込むと文字化けすることがある

* 解決方法
    * 読み込み時に文字コードを指定する方法
    * コマンドプロンプトをUTF-8対応に指定する方法
    
```bash
# 文字コードを指定する方法
mysql -u sample -p -defaultcharacter-set=utf8 sampledb < work.sql

# コマンドプロンプトをUTF-8対応に設定
chcp 65001
```

* `chcp`コマンド: Windowsのコマンドプロンプトの文字コードを確認する
    * `932` = `shift-JIS`
    * `65001` = `UTF-8`
