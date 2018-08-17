# 検索された数を調べる count

* 検索されたエンティティの数を調べて返すもの
* 返値は整数値になる
    * `${SQL}->count();`

```php
//エンティティ数を調べる
find ()
    ->count();
```

## サンプル

* 検索を実行する
* その最初と最後のエンティティのnameをメッセージとして表示する
* 検索されたエンティティ数をメッセージとして表示する

```php
public function find() {
    $this->set('msg', null);
    $persons = [];
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $first = $this->Persons->find()
            ->where(["name like "=>'%' . $find . '%'])
            ->first();
        $count = $last = $this->Persons->find()
            ->where(["name like "=>'%' . $find . '%'])
            ->count();
        $last = $this->Persons->find()
            ->offset($count - 1)
            ->where(["name like "=>'%' . $find . '%'])
            ->first();
        $persons = $this->Persons->find()
            ->where(["name like "=>'%' . $find . '%']);
        $msg =     'FIRST: '
                ". $first->name . "
                ', LAST: '
                " . $last->name . "
                '. ('
                .$cout .
                ')';
        $this->set('msg', $msg);
    }
    $this->set('persons', $persons);
}
```
