# OR検索する

* これも複数の条件を設定するのに使用
* こちらは、whereで設定した条件と別の条件のどちらかが片方が成立する場合に検索できるという場合に用いる

例えば、`IDが2か、名前が『AKI』のレコード`を検索する場合には、以下の２通りの書き方がある

* conditionsをキーにした連想配列にORをキーにした連想配列を作成する
* `orWhere()`で連結する

```php
//OR検索
find ('all', array(
    'conditions' => array(
        'OR' => array(
            'Persons.id' => 2, 'Persons.name' => '中会議室',
        )
    )
));
```

```php
//OR検索
find()
    ->where(["Persons.id=" => 2]),
    ->orWhere(["name LIKE "=>'%' . "AKI" . '%']);
```

これらの利用例

```php
public function find() {
    $this->set('msg', null);
    $persons = [];
    if ($this->request->is('post')) {
        $find = $this->request->data['find'];
        $persons = $this->Persons->find()
            ->where(["name like "=>'%' . $find . '%'])
            ->orWhere(["mail like "=>'%' . $find . '%']);
    }
    $this->set('persons', $persons);
}
```

ここでは、フィールドに検索テキストを書いて送信すると、nameかmailのどちらかにそのテキスト含む全てを検索する
