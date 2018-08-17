# QueryExpressionの利用

* [概要](00_about)
* [QueryExpressionで使えるメソッド](01)

## ues文

* QueryExpressionの利用は`use文`で追記しておく必要がある
* `ConnectionManager`は、`Cake/Datasource名前空間`に配置されている
* このuse文を追記しないとクラス名だけで利用不可

```diff
+ use Cake/Datasource/ConnectionManager;
```

## Connectionを得る

* 最初に、ConnectionManager`でConnection`インスタンスを取得する

```diff
+ $connetion = ConnectionManager::get('default');
```

## SQLクエリー文を作成する

* 実行するクエリーのテキストを用意
* `select * from persons where`の後に、送信されてきたテキストを繋げていく

```diff
$query = 'select * from persons where ' . $find;
```

## queryし、fetchAllする

* メソッドチェーンを使用
    * Connection`からquery`を呼び出し
    * `fetchAll()`で全エンティティを取得
    * 検索されあtレコードが配列の形で取り出される
* あとは、これをテンプレート側に渡して処理していくだけ
* ただし、`得られるデータの型式が異なる`

```diff
$persons = $connection->query($query)->fetchAll();
```
