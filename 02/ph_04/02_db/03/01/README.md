# SQLの標準の策定

* OracleがSQLを解析する時に、同じSQLであると判断するにはSQLの文字列を比較
    * そのため、大文字･小文字の違いや空白(スペース)の違いなどや、
    * SQL記述方法の違いによって、取得できる結果としては同じSQLだとしても、違うSQLだと判断されてしまう
* SQLを記述するにも開発プロジェクトで何らかの標準が必要になる
* プログラムからSQLの記述を統一させる方法として、`バインド変数の利用`がある

## バインド変数の利用

* JavaのJDBC APIであれば、PreparedStatement
* バインド変数を利用することで、SQL実行時の条件値が違っても、同じSQLだと認識させることができる

### 例: 商品を取得するSQL

```sql
--バインド変数なし (直接値を書き込む必要がある)
SELECT item_id, item_name FROM item WHERE item_category_id=10
--バインド変数あり (キャッシュが適用されてパフォーマンスが向上)
SELECT item_id, item_name FROM item WHERE item_category_id=?
```

### SQLの記述方法を標準化する

### 例: 内部結合を記述する方法

* 以下はSQLは全く同じ結果を返す
* 記述方法が異なるため、これらは`違うSQLとして判断`される

```sql
--INNER JOINを明示的に記述する方法
SELECT 
  item.item_id, item_category.item_category_name 
FROM 
  item 
INNER JOIN 
  item_category 
ON
  item.item_category_id = item_category_id;

--FROMに2つのテーブルを記述し、WHFRE句に結合条件を指定した記述方法
SELECT 
  item.item_id, item_category.item_category_name 
FROM 
  item, item_category 
WHERE
  item.item_category_id = item_category_id
```