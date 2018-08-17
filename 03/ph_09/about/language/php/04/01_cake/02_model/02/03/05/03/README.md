# NOT検索

さらに`IDが１でも、名前が『中会議室』でもないレコード』を検索するには、

```php
//NOT検索
find ('all', array(
    'conditions' => array(
        'NOT' => array(
            'MeetingRoom.id' => 2, 'MeetingRoom.name' => '中会議室',
        )
    )
));
```

と、絞り込み条件群を`NOT`というキー名の連想配列に入れてやる

これらの`Conditions`の中の`絞り込み条件`は、`多階層構造`にすることも可能`なので、例えば、`AND`の中に`OR`があったりしても大丈夫
