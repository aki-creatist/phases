# QueryExpressionで使えるメソッド

* `QueryExpression`クラスには、検索条件を設定するために様々なメソッドが用意されている
* これらのメソッドは、基本的にwhere内に条件として用意される演算記号(比較演算子)を使った式と同等の働きをする
* 最終的にデータベース・アクセスはSQLのクエリーとして実行される
* したがって、`どういうSQLのクエリーが生成されるのか`が頭に入っていれば、これらのメソッドの使い方もすぐに理解可能

## =,!=演算子

* 指定したフィールドの値が等しい、あるいは等しくない、という場合に用いる
* `=`、`!=`といった演算記号に相当するのが`eq()`、`notEq()`
* 例えば、`eq('name','taro')`というのは、`where 'name' = 'taro'`といったクエリーと同様

```php
eq( フィールド, 値 )
notEq( フィールド, 値 )
```

## >,>=演算子

* `フィールド > 値`あるいは`フィールド >= 値`
    * そのフィールドの値が、引数の値より大きいものを検索するためのもの

```php
gt( フィールド, 値 )
gte( フィールド, 値 )
```

## <,<=演算子

* `フィールド > 値`あるいは`フィールド >= 値`
    * そのフィールドの値が、引数の値より大きいものを検索するためのもの
    
```php
lt( フィールド, 値 )
lte( フィールド, 値 )
```

## = null, != null

* 指定したフィールドの値がnullかどうかをチェックするためのもの
    * 例: `isNotNull('name')`は、nameフィールドがnullでないものだけを検索する

```php
isNull( フィールド )
isNotNull( フィールド )
```

## like, notLike演算子

* あいまい検索(LIKE検索)を行うためのもの
    * 例: `like('name', '%ko')`は、`name like '%ko'`という条件式になる
        * nameの値が'ko'で終わるもの

```php
like( フィールド, 値 )
notLike( フィールド, 値 )
```

## in演算子

* フィールドの値が、用意した配列の値のいずれかと等しいものを検索するためのもの
    * 例えば、`in('name', ['taro','jiro','saburou'])`とする場合
        * `'name' in ('taro','jiro','saburou')`といったクエリーと同じ働きをするようになる

```php
in( フィールド, 配列 )
```

## 利用例

* ここでは、入力フィールドにカンマで区切って複数の名前を記入すると、それらのエンティティを全て取り出す
* この際、以下のことをチェック
    * `nameがnull`でないか？
    * `mailがnull`でないか？
    * `age`の値がゼロより大きいか？
* 全てをクリアしたエンティティだけが取り出される
* `fnc`に用意されている内容
    * メソッドチェーンを使って、`isNotNull`、`gt`、`in`といったメソッドを次々と呼び出している
* このようにして、より細かな検索条件の設定が行える

```php
public function find() {
    $persons = [];
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $query = $this->Persons->find();
        $exp = $query->newExpr();
        $fnc = function($exp, $f) {
            return $exp
                ->isNotNull('name')
                ->isNotNull('mail')
                ->gt('age',0)
                ->in('name', explode(',',$f));
        };
        $persons = $query->where($fnc($exp,$find));
    }
    $this->set('persons,$persons);
    $this->set('msg',null);
}
```
