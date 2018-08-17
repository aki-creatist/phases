# AND検索する

複数の条件を設定したい場合に使うもの

* `whereで設定した条件 + 別の条件の両方が成立する`ものを取り出す
* 使い方は基本的にwhereと同じ
* 書き方は以下の3通り
    * conditionsに連想配列で並列に並べる
    * conditionsをキーにした連想配列にANDをキーにした連想配列を作成する
    * `andWhere()`で連結する

```php
find ('all', array(
    'conditions' => array(
        'Persons.id' => 2, 'Persons.name' => 'AKI',
    )
));
```

```php
find ('all', array(
    'conditions' => array(
        'AND' => array( //絞り込み条件群を`AND`というキー名の`連想配列`に入れる
            'Persons.id' => 2, 'Persons.name' => 'AKI',
        )
    )
));
```

```php
find ()
    ->where(["Persons.id"=> 2]),
    ->andWhere(["Persons.name like "=>'%' . "AKI" . '%']); //両方の条件に合うものだけが検索される
```
