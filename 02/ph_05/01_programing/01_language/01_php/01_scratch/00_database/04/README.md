# プリペアドステートメント

## 概要

* 速度と安全性を向上する仕組み
    * SQL文のテンプレートを先に準備(prepare)し、値とSQL部分を分離
* SQL文と外部の値を区別する
    * 値の部分に`プレースホルダ`と呼ばれる識別子を置く

## プレースホルダ

* プレースホルダには２種類ある
    * `:名前`形式の名前付きプレースホルダ
    * `?`プレースホルダ
    
## プレースホルダを利用して組み立てる

* 外部から届くデータの部分(グローバル変数)をプレースホルダを利用して置き換えている
* 名前付きプレースホルダは、`:`とカラム名`last_name`を組み合わせて`:last_name`としている
* 他のカラムも同様に指定する

```php
// `:名前`を使う場合
$sql = "INSERT INTO member ( last_name, first_name, age,)
    VALUES ( :last_name, :first_name, :age,)";
```

`?`プレースホルダは、値の部分に`?`を指定するだけ

```php
// `?`を使う場合
$sql = "INSERT INTO member ( last_name, first_name, age,)
    VALUES ( ?, ?, ?,)";
```

## 値を結びつける

* `prepare()`で前の手順で作成したSQLを引数に設定して実行するとSQLを解析してキャッシュする
* 同じSQLを実行する時に速度が改善されるのは二度目以降はこのキャッシュを利用する
    * そのため次にSQLの各々のプレースホルダと値をバインド(結びつける)する利用できる
    * メソッドは２つ
        * `bindValue`
        * `bindParam`

ここでは動作がわかりやすいbindValueと名前付きプレースホルダを利用する

* `$pdo`にPDOクラスのオブジェクトが格納されているとする
* `prepare()`で$sqlに格納されたSQL文を解析する
* 返り値としてステートメントハンドラ(PDOStatementクラスのオブジェクト)が返り、$stmhに格納される

```php
$stmh = $pdo->prepare($sql);
```

* PDOStatementクラスの`bindValue()`を利用
* 第一引数にプレースホルダを使った名前を、第二引数に外部から送信された値を指定する
* `bindValue()`の中の識別し`:last_name`は`'`で囲ってる

```php
$stmh->bindValue(':last_name',  $_POST['last_name']);
$stmh->bindValue(':first_name', $_POST['first_name']);
$stmh->bindValue(':age',        $_POST['age']);
```

* 準備ができたらPDOStatementクラスの`execute()`でSQL文を実行する

```php
$stmh->execute();
```

* `?`プレースホルダの場合は`?`に対応する部分に数字を順番に記述する

```php
$sql = "INSERT  INTO member (last_name, first_name, age) VALUES ( ?, ?, ?)";
$stmh = $pdo->prepare($sql);
$stmh->bindValue( 1, $_POST['last_name']);
$stmh->bindValue( 2, $_POST['first_name']);
$stmh->bindValue( 3, $_POST['age']);
$stmh->execute();
```
