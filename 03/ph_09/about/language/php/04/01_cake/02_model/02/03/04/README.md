# フィールドを指定する(fieldsとselect)

多数のエンティティを受け取る際に、`どういう形で受け取るか`

* 全てのフィールドを取り出すのでなく、テーブルにあるフィールドから必要な項目だけを指定して取り出する
* ここでは２通りの書き方を示する
    * `検索条件`に`fields`というキー名の連想配列を設定する
    * `select()`を利用する

## fields

`検索条件`に`fields`というキー名の連想配列を設定することで指定したフィールドのみ取り出す

```php
//fieldsでカラムを選択する
public function find() {
    $this->set('msg', null);
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $persons = $this->Persons->find('all',array(
            'fields' => array(
                'id','name'
            ),
            'conditions' => array(
                'name LIKE' => $find
            )
        ));
    } else {
        $persons = [];
    }
    $this->set('persons', $person);
}
```

## select()

* `select()`は取り出すフィールドを指定する
* `《Query》->select([ field1, field2, ...])`の書き方

```php
//selectでカラムを選択する
public function find() {
    $this->set('msg', null);
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $persons = $this->Persons->find()
            ->select(['id', 'name'])
            ->where(["name LIKE "=> '%' . $find . '%']);
    } else {
        $persons = [];
    }
    $this->set('persons', $person);
}
```

* 引数には、取り出したいフィールド名をまとめた配列を用意して
* 行なっていることはどちらも同じ