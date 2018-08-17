## SQL文の組立の基本

以下のコードはデータを登録する時のINSERT文

* `値が直接記述されているSQL文`はターミナルやコマンドプロンプトから入力するように記述する場合

```php
// 値が直接記述されているSQL文
$sql = 'INSERT INTO member ( last_name, first_name, age,) VALUES ( '田中', '一郎', 21)";
```

* 会員登録フォームでユーザーがデータを送信するような場合
    * 外部から送信されたデータをSQLに組み込む必要がある
    * 攻撃に利用される`SQLとして意味のある文字(`'`など)を無効化する必要がある

```php
// 値がグローバル変数で記述されているSQL文
$sql = 'INSERT INTO member ( last_name, first_name, age,)
    VALUES ( '".$_POST['last_name'] . "',
             '".$_POST['first_name'] . "',
             '".$_POST['first_name'] . "')";
```
