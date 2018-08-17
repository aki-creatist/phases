# 概要

* 複雑な検索を行う
* `QueryExpression`を利用する
    * メソッドチェーンで呼び出で複雑な条件を作成可能
    * クエリー表現を作成するための絹を提供するクラス
        * `$変数 = 《Query》->newExpr();`
* 条件を設定するためのメソッドが色々と用意されている
    * これらのメソッドを呼び出し、その結果を利用することで複雑な条件が作成可能
* `where()`で結果を利用する
* `where()`は`QueryExpression`の指定も可能

下のサンプルは、`find()`を修正し、ageを使って検索するようにしたもの

```php
public function find() {
    $persons = [];
    if ($this->request->is('post')){
        $find = $this->request->data['find'];
        $query = $this->Persons->find();
        $exp = $query->newExpr();
        $fnc = function($exp, $find) {
            return $exp->get('age', $find * 1);
        };
        $persons = $query->where($fnc($exp, $find));
    }
    $this->set('persons', $persons);
    $this->set('msg', null);
}
```

* 例: `20`と入力して送信すると、ageが20以上のものだけが検索される
* ここでは、`$fnc`という`無名関数`を用意
    * `QueryExpression`を`$exp`に渡す
    * `検索テキスト`を`$find`に渡すして呼び出す
    
```php
$fnc = function($exp, $find) {
    return $exp->get('age', $find * 1);
};
```

* この中で、QueryExpressionの`get()`を使って検索条件を設定
* 実際に検索を行う際には、まず`Query`と`QueryExpression`をそれぞれ変数に代入しておく

```php
$query = $this->Persons->find();
$exp = $query->newExpr();
```

* これで一通りの準備完了
* 実際の検索は`where`を使って行う
* この引数に先ほどの無名関数`$fnc`を指定してやればいい
    * `$persons = $query->where($fnc($exp,$find));`

これで、fnc`関数の結果がwhere`に引数として指定され、その結果、`age`の値が`$find`以上のものだけが`$persons`に返される
